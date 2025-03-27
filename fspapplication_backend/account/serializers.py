from rest_framework import serializers
from .models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    # Map backend fields to frontend expected fields
    addressLine1 = serializers.SerializerMethodField()
    addressLine2 = serializers.SerializerMethodField()
    postalCode = serializers.CharField(source='postal_code')
    phoneNumber = serializers.CharField(source='phone_number')
    emergencyContact = serializers.CharField(source='emergency_contact')
    emergencyContactFirstName = serializers.CharField(source='emergency_contact_first_name')
    emergencyContactLastName = serializers.CharField(source='emergency_contact_last_name')
    
    class Meta:
        model = UserProfile
        fields = ('phoneNumber', 'country', 'city', 'state', 'postalCode', 
                 'addressLine1', 'addressLine2', 'latitude', 'longitude',
                 'emergencyContact', 'emergencyContactFirstName', 'emergencyContactLastName')
    
    def get_addressLine1(self, obj):
        # Combine street_number and street_name for addressLine1
        street_parts = []
        if obj.street_number:
            street_parts.append(obj.street_number)
        if obj.street_name:
            street_parts.append(obj.street_name)
        return " ".join(street_parts) if street_parts else ""
    
    def get_addressLine2(self, obj):
        # Use unit_number as addressLine2
        return obj.unit_number if obj.unit_number else ""

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    
    class Meta:
        model = User
        fields = ('id', 'firstName', 'lastName', 'email', 'profile') 
