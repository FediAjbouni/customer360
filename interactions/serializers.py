from rest_framework import serializers
from .models import Interaction
from customer_management.serializers import CustomerListSerializer


class InteractionSerializer(serializers.ModelSerializer):
    """
    Serializer for Interaction model with nested customer data.
    """
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    channel_display = serializers.CharField(source='get_channel_display', read_only=True)
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Interaction
        fields = [
            'id', 'customer', 'customer_name', 'customer_email',
            'channel', 'channel_display', 'direction', 'direction_display',
            'status', 'status_display', 'interaction_date', 'summary', 'notes', 'created_by'
        ]
        read_only_fields = ['id', 'interaction_date']

    def validate_summary(self, value):
        """Validate interaction summary."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Summary must be at least 10 characters long.")
        return value.strip()


class InteractionListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for interaction lists.
    """
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    channel_display = serializers.CharField(source='get_channel_display', read_only=True)
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    
    class Meta:
        model = Interaction
        fields = [
            'id', 'customer_name', 'channel', 'channel_display',
            'direction', 'direction_display', 'interaction_date', 'summary'
        ]


class InteractionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating interactions with minimal fields.
    """
    
    class Meta:
        model = Interaction
        fields = ['customer', 'channel', 'direction', 'status', 'summary', 'notes', 'created_by']

    def validate_summary(self, value):
        """Validate interaction summary."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Summary must be at least 10 characters long.")
        return value.strip()