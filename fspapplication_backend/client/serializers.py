from rest_framework import serializers
from .models import Client, ClientWarehouse, ClientContact

class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model.
    Used for listing, retrieving, creating, and updating clients.
    """
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'abn', 'website',
            'email', 'phone', 'street_number', 'street_name', 'suburb', 
            'city', 'state', 'postal_code', 'country', 'latitude', 'longitude',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 