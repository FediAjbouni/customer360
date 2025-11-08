from django.contrib import admin
from django.utils.html import format_html
from .models import Interaction


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Interaction model.
    """
    list_display = [
        'customer_name', 'channel_display', 'direction_display', 
        'status_display', 'interaction_date', 'created_by'
    ]
    list_filter = [
        'channel', 'direction', 'status', 'interaction_date',
        ('customer', admin.RelatedOnlyFieldListFilter)
    ]
    search_fields = [
        'customer__name', 'customer__email', 'summary', 
        'notes', 'created_by'
    ]
    readonly_fields = ['interaction_date']
    list_per_page = 30
    date_hierarchy = 'interaction_date'
    raw_id_fields = ['customer']
    
    fieldsets = (
        ('Interaction Details', {
            'fields': ('customer', 'channel', 'direction', 'status')
        }),
        ('Content', {
            'fields': ('summary', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_by', 'interaction_date'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_pending', 'mark_as_follow_up']

    def customer_name(self, obj):
        """Display customer name with link."""
        return format_html(
            '<a href="/admin/customer_management/customer/{}/change/">{}</a>',
            obj.customer.id, obj.customer.name
        )
    
    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'customer__name'

    def channel_display(self, obj):
        """Display channel with icon."""
        icons = {
            'phone': '📞',
            'sms': '💬',
            'email': '📧',
            'letter': '✉️',
            'social_media': '📱',
            'in_person': '👥',
            'chat': '💭'
        }
        icon = icons.get(obj.channel, '📋')
        return f"{icon} {obj.get_channel_display()}"
    
    channel_display.short_description = 'Channel'
    channel_display.admin_order_field = 'channel'

    def direction_display(self, obj):
        """Display direction with color coding."""
        if obj.direction == 'inbound':
            return format_html('<span style="color: green;">⬇️ Inbound</span>')
        else:
            return format_html('<span style="color: blue;">⬆️ Outbound</span>')
    
    direction_display.short_description = 'Direction'
    direction_display.admin_order_field = 'direction'

    def status_display(self, obj):
        """Display status with badge styling."""
        colors = {
            'pending': 'orange',
            'completed': 'green',
            'follow_up': 'blue'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">● {}</span>',
            color, obj.get_status_display()
        )
    
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'

    def mark_as_completed(self, request, queryset):
        """Bulk mark interactions as completed."""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} interactions marked as completed.')
    
    mark_as_completed.short_description = "Mark as completed"

    def mark_as_pending(self, request, queryset):
        """Bulk mark interactions as pending."""
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} interactions marked as pending.')
    
    mark_as_pending.short_description = "Mark as pending"

    def mark_as_follow_up(self, request, queryset):
        """Bulk mark interactions as requiring follow-up."""
        updated = queryset.update(status='follow_up')
        self.message_user(request, f'{updated} interactions marked as requiring follow-up.')
    
    mark_as_follow_up.short_description = "Mark as follow-up required"

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related('customer')