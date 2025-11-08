from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
import logging

from .models import Interaction
from .forms import InteractionForm, InteractionFilterForm
from customer_management.models import Customer

logger = logging.getLogger(__name__)


class InteractionListView(ListView):
    """
    Display list of interactions with filtering and pagination.
    """
    model = Interaction
    template_name = 'interactions/interaction_list.html'
    context_object_name = 'interactions'
    paginate_by = 25

    def get_queryset(self):
        queryset = Interaction.objects.select_related('customer').all()
        
        # Apply filters
        customer_id = self.request.GET.get('customer')
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        channel = self.request.GET.get('channel')
        if channel:
            queryset = queryset.filter(channel=channel)
        
        direction = self.request.GET.get('direction')
        if direction:
            queryset = queryset.filter(direction=direction)
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        date_from = self.request.GET.get('date_from')
        if date_from:
            queryset = queryset.filter(interaction_date__date__gte=date_from)
        
        date_to = self.request.GET.get('date_to')
        if date_to:
            queryset = queryset.filter(interaction_date__date__lte=date_to)
        
        return queryset.order_by('-interaction_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = InteractionFilterForm(self.request.GET)
        context['total_interactions'] = Interaction.objects.count()
        return context


class InteractionDetailView(DetailView):
    """
    Display detailed view of an interaction.
    """
    model = Interaction
    template_name = 'interactions/interaction_detail.html'
    context_object_name = 'interaction'


class InteractionCreateView(CreateView):
    """
    Create a new interaction.
    """
    model = Interaction
    form_class = InteractionForm
    template_name = 'interactions/interaction_form.html'
    success_url = reverse_lazy('interactions:interaction_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass customer_id if provided in URL
        kwargs['customer_id'] = self.kwargs.get('customer_id')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.kwargs.get('customer_id')
        if customer_id:
            context['customer'] = get_object_or_404(Customer, id=customer_id)
        return context

    def form_valid(self, form):
        logger.info(f"Creating new interaction for customer: {form.cleaned_data['customer'].name}")
        messages.success(self.request, "Interaction recorded successfully!")
        return super().form_valid(form)


class InteractionUpdateView(UpdateView):
    """
    Update an existing interaction.
    """
    model = Interaction
    form_class = InteractionForm
    template_name = 'interactions/interaction_form.html'
    success_url = reverse_lazy('interactions:interaction_list')

    def form_valid(self, form):
        logger.info(f"Updating interaction ID: {self.object.pk}")
        messages.success(self.request, "Interaction updated successfully!")
        return super().form_valid(form)


class InteractionDeleteView(DeleteView):
    """
    Delete an interaction.
    """
    model = Interaction
    template_name = 'interactions/interaction_confirm_delete.html'
    success_url = reverse_lazy('interactions:interaction_list')

    def delete(self, request, *args, **kwargs):
        logger.info(f"Deleting interaction ID: {self.get_object().pk}")
        messages.success(request, "Interaction deleted successfully!")
        return super().delete(request, *args, **kwargs)


def summary_view(request):
    """
    Display interaction summary and analytics.
    """
    try:
        # Date range for analysis
        thirty_days_ago = date.today() - timedelta(days=30)
        seven_days_ago = date.today() - timedelta(days=7)
        
        # Basic statistics
        total_interactions = Interaction.objects.count()
        interactions_30_days = Interaction.objects.filter(
            interaction_date__date__gte=thirty_days_ago
        ).count()
        interactions_7_days = Interaction.objects.filter(
            interaction_date__date__gte=seven_days_ago
        ).count()
        
        # Channel breakdown (last 30 days)
        channel_stats = Interaction.objects.filter(
            interaction_date__date__gte=thirty_days_ago
        ).values('channel', 'direction').annotate(
            count=Count('id')
        ).order_by('channel', 'direction')
        
        # Status breakdown
        status_stats = Interaction.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Top customers by interaction count (last 30 days)
        top_customers = Customer.objects.filter(
            interactions__interaction_date__date__gte=thirty_days_ago
        ).annotate(
            interaction_count=Count('interactions')
        ).order_by('-interaction_count')[:10]
        
        context = {
            'total_interactions': total_interactions,
            'interactions_30_days': interactions_30_days,
            'interactions_7_days': interactions_7_days,
            'channel_stats': channel_stats,
            'status_stats': status_stats,
            'top_customers': top_customers,
            'date_range': f"{thirty_days_ago.strftime('%Y-%m-%d')} to {date.today().strftime('%Y-%m-%d')}"
        }
        
        logger.info(f"Generated summary with {total_interactions} total interactions")
        return render(request, 'interactions/summary.html', context)
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        messages.error(request, "An error occurred while generating the summary.")
        return render(request, 'interactions/summary.html', {
            'total_interactions': 0,
            'interactions_30_days': 0,
            'interactions_7_days': 0,
            'channel_stats': [],
            'status_stats': [],
            'top_customers': []
        })


# Legacy function-based views for backward compatibility
def interact(request, cid):
    """Legacy view - redirects to new interaction create view."""
    return redirect('interactions:interaction_create_for_customer', customer_id=cid)


def summary(request):
    """Legacy view - use the new summary_view."""
    return summary_view(request)