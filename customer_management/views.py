from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
import logging

from .models import Customer
from .forms import CustomerForm, CustomerSearchForm

logger = logging.getLogger(__name__)


class CustomerListView(ListView):
    """
    Display list of customers with search and pagination.
    """
    model = Customer
    template_name = 'customer_management/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20

    def get_queryset(self):
        queryset = Customer.objects.all().annotate(
            total_interactions=Count('interactions')
        )
        
        # Handle Active Only filter
        is_active_filter = self.request.GET.get('is_active')
        if is_active_filter == 'on':  # Checkbox is checked
            queryset = queryset.filter(is_active=True)
        elif is_active_filter is None:  # Default behavior - show active only
            queryset = queryset.filter(is_active=True)
        # If is_active_filter == '' (unchecked), show all customers
        
        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query)
            )
        
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = CustomerSearchForm(self.request.GET)
        
        # Calculate total customers based on current filter
        is_active_filter = self.request.GET.get('is_active')
        if is_active_filter == 'on' or is_active_filter is None:
            context['total_customers'] = Customer.objects.filter(is_active=True).count()
        else:
            context['total_customers'] = Customer.objects.count()
            
        return context


class CustomerDetailView(DetailView):
    """
    Display detailed view of a customer with their interactions.
    """
    model = Customer
    template_name = 'customer_management/customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        
        # Get recent interactions
        recent_interactions = customer.interactions.all()[:10]
        context['recent_interactions'] = recent_interactions
        
        # Get interaction statistics
        context['interaction_stats'] = {
            'total': customer.interactions.count(),
            'this_month': customer.interactions.filter(
                interaction_date__month=timezone.now().month
            ).count(),
        }
        
        return context


class CustomerCreateView(CreateView):
    """
    Create a new customer.
    """
    model = Customer
    form_class = CustomerForm
    template_name = 'customer_management/customer_form.html'
    success_url = reverse_lazy('customer_management:customer_list')

    def form_valid(self, form):
        logger.info(f"Creating new customer: {form.cleaned_data['name']}")
        messages.success(self.request, f"Customer '{form.cleaned_data['name']}' created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Invalid customer form submission: {form.errors}")
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class CustomerUpdateView(UpdateView):
    """
    Update an existing customer.
    """
    model = Customer
    form_class = CustomerForm
    template_name = 'customer_management/customer_form.html'
    success_url = reverse_lazy('customer_management:customer_list')

    def form_valid(self, form):
        logger.info(f"Updating customer: {form.cleaned_data['name']} (ID: {self.object.pk})")
        messages.success(self.request, f"Customer '{form.cleaned_data['name']}' updated successfully!")
        return super().form_valid(form)


class CustomerDeleteView(DeleteView):
    """
    Soft delete a customer (mark as inactive).
    """
    model = Customer
    template_name = 'customer_management/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_management:customer_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add interaction count for display in template
        context['interaction_count'] = self.object.interactions.count()
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Soft delete - mark as inactive instead of actual deletion
        self.object.is_active = False
        self.object.save()
        
        logger.info(f"Soft deleted customer: {self.object.name} (ID: {self.object.pk})")
        messages.success(request, f"Customer '{self.object.name}' has been deactivated.")
        return redirect(self.success_url)


# API Views for AJAX requests
def customer_search_api(request):
    """
    API endpoint for customer search (for AJAX autocomplete).
    """
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'customers': []})
    
    customers = Customer.objects.filter(
        Q(name__icontains=query) | Q(email__icontains=query),
        is_active=True
    )[:10]
    
    customer_data = [
        {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone
        }
        for customer in customers
    ]
    
    return JsonResponse({'customers': customer_data})


# Legacy function-based views for backward compatibility
def index(request):
    """Legacy view - redirects to new customer list view."""
    return redirect('customer_management:customer_list')


def create_customer(request):
    """Legacy view - redirects to new customer create view."""
    return redirect('customer_management:customer_create')