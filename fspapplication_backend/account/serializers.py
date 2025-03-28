from rest_framework import serializers
from .models import User, UserProfile, EmployeeProfile, FunctionalGroup

class UserProfileSerializer(serializers.ModelSerializer):
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
        street_parts = []
        if obj.street_number:
            street_parts.append(obj.street_number)
        if obj.street_name:
            street_parts.append(obj.street_name)
        return " ".join(street_parts) if street_parts else ""
    
    def get_addressLine2(self, obj):
        return obj.unit_number if obj.unit_number else ""

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    
    class Meta:
        model = User
        fields = ('id', 'firstName', 'lastName', 'email', 'profile', 'user_type', 'avatar') 

class UserListSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    fullName = serializers.SerializerMethodField()
    userType = serializers.CharField(source='user_type')
    functionalGroups = serializers.SerializerMethodField()
    employeeDetails = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 
            'firstName', 
            'lastName', 
            'fullName',
            'email', 
            'userType', 
            'avatar', 
            'functionalGroups',
            'employeeDetails',
            'is_active',
            'date_joined'
        )
    
    def get_fullName(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def get_functionalGroups(self, obj):
        return list(obj.functional_groups.values_list('name', flat=True))
    
    def get_employeeDetails(self, obj):
        try:
            profile = obj.employee_profile
            return {
                'company': profile.company.name if profile.company else None,
                'department': profile.department,
                'jobTitle': profile.job_title,
                'startDate': profile.start_date
            }
        except AttributeError:
            return None 
