from rest_framework import serializers
from .models import Agent, AgentWarehouse

class AgentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Agent model.
    Used for listing, retrieving, creating, and updating agents.
    """
    class Meta:
        model = Agent
        fields = [
            'id', 'name', 'logo', 'abn', 'website',
            'email', 'phone', 'street_number', 'street_name', 'suburb', 
            'city', 'state', 'postal_code', 'country', 'latitude', 'longitude',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AgentWarehouseSerializer(serializers.ModelSerializer):
    """
    Serializer for the AgentWarehouse model.
    Used for listing, retrieving, creating, and updating agent warehouses.
    """
    class Meta:
        model = AgentWarehouse
        fields = [
            'id', 'agent', 'name', 'description', 
            'street_number', 'street_name', 'suburb', 'city', 'state', 
            'postal_code', 'country', 'latitude', 'longitude',
            'first_name', 'last_name', 'contact_phone', 'contact_email',
            'is_primary', 'operating_hours', 'facility_type', 'special_instructions',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 