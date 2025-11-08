from django import forms
from django.core.exceptions import ValidationError
from .models import Interaction
from customer_management.models import Customer


class InteractionForm(forms.ModelForm):
    """
    Enhanced form for creating and editing interactions.
    """
    
    class Meta:
        model = Interaction
        fields = ['customer', 'channel', 'direction', 'status', 'summary', 'notes', 'created_by']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'channel': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'direction': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the interaction...',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes (optional)...'
            }),
            'created_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name or ID'
            }),
        }

    def __init__(self, *args, **kwargs):
        customer_id = kwargs.pop('customer_id', None)
        super().__init__(*args, **kwargs)
        
        # If customer_id is provided, set it as initial and hide the field
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
                self.fields['customer'].initial = customer
                self.fields['customer'].widget = forms.HiddenInput()
            except Customer.DoesNotExist:
                pass

    def clean_summary(self):
        """Validate interaction summary."""
        summary = self.cleaned_data.get('summary')
        if summary:
            summary = summary.strip()
            if len(summary) < 10:
                raise ValidationError("Summary must be at least 10 characters long.")
        return summary


class InteractionFilterForm(forms.Form):
    """
    Form for filtering interactions.
    """
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_active=True),
        required=False,
        empty_label="All Customers",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    channel = forms.ChoiceField(
        choices=[('', 'All Channels')] + Interaction.CHANNEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    direction = forms.ChoiceField(
        choices=[('', 'All Directions')] + Interaction.DIRECTION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Interaction.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )