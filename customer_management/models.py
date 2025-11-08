from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse


class Customer(models.Model):
    """
    Customer model with enhanced validation and methods.
    """
    name = models.CharField(
        max_length=100,
        help_text="Customer's full name"
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        help_text="Customer's email address"
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        help_text="Customer's phone number"
    )
    address = models.CharField(
        max_length=200,
        help_text="Customer's address"
    )
    social_media = models.CharField(
        max_length=100,
        blank=True,
        help_text="Customer's social media handle (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.name} ({self.email})"

    def get_absolute_url(self):
        return reverse('customer_management:customer_detail', kwargs={'pk': self.pk})

    @property
    def interaction_count(self):
        """Return the total number of interactions for this customer."""
        return self.interactions.count()

    @property
    def last_interaction(self):
        """Return the most recent interaction for this customer."""
        return self.interactions.order_by('-interaction_date').first()