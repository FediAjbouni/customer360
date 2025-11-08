from django.contrib import admin
from django.utils.html import format_html
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Customer model.
    """
    list_display = [
        'name', 'email', 'phone', 'interaction_count_display', 
        'is_active', 'created_at', 'last_interaction_display'
    ]
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at', 'interaction_count', 'last_interaction']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Contact Details', {
            'fields': ('address', 'social_media')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'interaction_count', 'last_interaction'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_customers', 'deactivate_customers']

    def interaction_count_display(self, obj):
        """Display interaction count with badge styling."""
        count = obj.interaction_count
        if count == 0:
            return format_html('<span class="badge badge-secondary">0</span>')
        elif count < 5:
            return format_html('<span class="badge badge-info">{}</span>', count)
        elif count < 10:
            return format_html('<span class="badge badge-warning">{}</span>', count)
        else:
            return format_html('<span class="badge badge-success">{}</span>', count)
    
    interaction_count_display.short_description = 'Interactions'
    interaction_count_display.admin_order_field = 'interactions__count'

    def last_interaction_display(self, obj):
        """Display last interaction date."""
        last_interaction = obj.last_interaction
        if last_interaction:
            return last_interaction.interaction_date.strftime('%Y-%m-%d %H:%M')
        return '-'
    
    last_interaction_display.short_description = 'Last Interaction'

    def activate_customers(self, request, queryset):
        """Bulk activate customers."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} customers were successfully activated.')
    
    activate_customers.short_description = "Activate selected customers"

    def deactivate_customers(self, request, queryset):
        """Bulk deactivate customers."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} customers were successfully deactivated.')
    
    deactivate_customers.short_description = "Deactivate selected customers"

    def get_queryset(self, request):
        """Optimize queryset with prefetch_related."""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('interactions')