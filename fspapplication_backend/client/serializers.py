from rest_framework import serializers
from .models import Client, ClientWarehouse, ClientContract

class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model.
    Used for listing, retrieving, creating, and updating clients.
    """
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'logo', 'abn', 'website',
            'email', 'phone', 'street_number', 'street_name', 'suburb', 
            'city', 'state', 'postal_code', 'country', 'latitude', 'longitude',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClientWarehouseSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClientWarehouse model.
    Used for listing, retrieving, creating, and updating client warehouses.
    """
    class Meta:
        model = ClientWarehouse
        fields = [
            'id', 'client', 'name', 'description', 
            'street_number', 'street_name', 'suburb', 'city', 'state', 
            'postal_code', 'country', 'latitude', 'longitude',
            'contact_name', 'contact_phone', 'contact_email',
            'is_primary', 'operating_hours', 'storage_capacity', 'special_instructions',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClientContractSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClientContract model.
    Used for listing, retrieving, creating, and updating client contracts.
    """
    class Meta:
        model = ClientContract
        fields = ['id', 'client', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at'] 