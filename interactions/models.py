from django.db import models
from django.urls import reverse
from customer_management.models import Customer


class Interaction(models.Model):
    """
    Interaction model to track customer communications.
    """
    CHANNEL_CHOICES = [
        ('phone', 'Phone'),
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('letter', 'Letter'),
        ('social_media', 'Social Media'),
        ('in_person', 'In Person'),
        ('chat', 'Live Chat'),
    ]

    DIRECTION_CHOICES = [
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('follow_up', 'Follow-up Required'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='interactions',
        help_text="Customer involved in this interaction"
    )
    channel = models.CharField(
        max_length=15,
        choices=CHANNEL_CHOICES,
        help_text="Communication channel used"
    )
    direction = models.CharField(
        max_length=10,
        choices=DIRECTION_CHOICES,
        help_text="Direction of communication"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='completed',
        help_text="Status of the interaction"
    )
    interaction_date = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(help_text="Summary of the interaction")
    notes = models.TextField(
        blank=True,
        help_text="Additional notes (optional)"
    )
    created_by = models.CharField(
        max_length=100,
        blank=True,
        help_text="User who created this interaction"
    )

    class Meta:
        ordering = ['-interaction_date']
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'

    def __str__(self):
        return f"{self.customer.name} - {self.get_channel_display()} ({self.interaction_date.strftime('%Y-%m-%d')})"

    def get_absolute_url(self):
        return reverse('interactions:interaction_detail', kwargs={'pk': self.pk})