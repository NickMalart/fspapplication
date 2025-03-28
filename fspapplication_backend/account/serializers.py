from rest_framework import serializers
from .models import User, UserProfile, EmployeeProfile, FunctionalGroup

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'phone_number', 
            'emergency_contact',
            'emergency_contact_first_name',
            'emergency_contact_last_name',
            'street_number',
            'street_name',
            'suburb',
            'city',
            'state',
            'postal_code',
            'country',
            'latitude',
            'longitude',
            'google_place_id',
            'date_of_birth'
        )

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'profile'
        )
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Update User instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update UserProfile instance
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    functional_groups = serializers.SerializerMethodField()
    employee_details = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'full_name',
            'email', 
            'user_type', 
            'avatar', 
            'functional_groups',
            'employee_details',
            'is_active',
            'date_joined'
        )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def get_functional_groups(self, obj):
        return list(obj.functional_groups.values_list('name', flat=True))
    
    def get_employee_details(self, obj):
        try:
            profile = obj.employee_profile
            return {
                'company': profile.company.name if profile.company else None,
                'department': profile.department,
                'job_title': profile.job_title,
                'start_date': profile.start_date
            }
        except AttributeError:
            return None 
