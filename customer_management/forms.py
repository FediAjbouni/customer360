from django import forms
from django.core.exceptions import ValidationError
from .models import Customer


class CustomerForm(forms.ModelForm):
    """
    Enhanced form for customer creation and editing with custom validation.
    """
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'social_media']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890',
                'required': True
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full address',
                'required': True
            }),
            'social_media': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username or profile URL (optional)'
            }),
        }

    def clean_name(self):
        """Validate customer name."""
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 2:
                raise ValidationError("Name must be at least 2 characters long.")
            if not name.replace(' ', '').isalpha():
                raise ValidationError("Name should only contain letters and spaces.")
        return name

    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            # Check for existing email (excluding current instance if editing)
            existing = Customer.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError("A customer with this email already exists.")
        return email

    def clean_social_media(self):
        """Clean and validate social media field."""
        social_media = self.cleaned_data.get('social_media')
        if social_media:
            social_media = social_media.strip()
            # Basic validation for social media handles
            if social_media and not (social_media.startswith('@') or 'http' in social_media):
                # If it doesn't start with @ or contain http, assume it's a username
                social_media = f"@{social_media}"
        return social_media


class CustomerSearchForm(forms.Form):
    """
    Form for searching customers.
    """
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, or phone...',
        })
    )
    
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )