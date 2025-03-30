from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'logo', 
            'number', 'street', 'city', 'state', 'postal_code', 'country',
            'latitude', 'longitude',
            'phone', 'email', 'website',
            'tax_number', 'abn_number',
            'primary_color', 'secondary_color',
            'established_date', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
