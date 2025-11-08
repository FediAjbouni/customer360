from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model with additional computed fields.
    """
    interaction_count = serializers.ReadOnlyField()
    last_interaction_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'phone', 'address', 'social_media',
            'created_at', 'updated_at', 'is_active',
            'interaction_count', 'last_interaction_date'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_interaction_date(self, obj):
        """Get the date of the last interaction."""
        last_interaction = obj.last_interaction
        return last_interaction.interaction_date if last_interaction else None

    def validate_email(self, value):
        """Validate email uniqueness."""
        if self.instance:
            # Editing existing customer
            if Customer.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A customer with this email already exists.")
        else:
            # Creating new customer
            if Customer.objects.filter(email=value).exists():
                raise serializers.ValidationError("A customer with this email already exists.")
        return value


class CustomerListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for customer lists.
    """
    interaction_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'interaction_count', 'is_active']