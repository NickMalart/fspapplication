from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    """Serializer for the Company model with camelCase field names for frontend compatibility"""
    companyName = serializers.CharField(source='name')
    addressLine1 = serializers.CharField(source='address_line1')
    addressLine2 = serializers.CharField(source='address_line2')
    postalCode = serializers.CharField(source='postal_code')
    abnNumber = serializers.CharField(source='abn_number')
    taxNumber = serializers.CharField(source='tax_number')
    primaryColor = serializers.CharField(source='primary_color')
    secondaryColor = serializers.CharField(source='secondary_color')
    establishedDate = serializers.DateField(source='established_date')
    
    class Meta:
        model = Company
        fields = (
            'id', 'companyName', 'logo', 'addressLine1', 'addressLine2', 
            'city', 'state', 'postalCode', 'country', 'phone', 'email', 
            'website', 'abnNumber', 'taxNumber', 'primaryColor', 
            'secondaryColor', 'establishedDate', 'created_at', 'updated_at'
        ) 