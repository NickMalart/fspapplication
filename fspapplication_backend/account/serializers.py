from rest_framework import serializers
from .models import User
from rest_framework import serializers
from django.apps import apps as django_apps  # Renamed to avoid conflict
from account.models import User  # Import shared User model
from .models import UserProfile, AgentProfile, ClientProfile, EmployeeProfile # Import tenant models

class LoginUserSerializer(serializers.ModelSerializer):
    """Serializer for basic user login information"""
    class Meta:
        model = User
        fields = ('id', 'email')
        read_only_fields = ('id',)

# Moved from account/serializers.py
class ProfileDataSerializer(serializers.ModelSerializer):
    """Serializer for user profile data only"""
    class Meta:
        model = UserProfile
        exclude = ('user',) 

# Moved from account/serializers.py
class CompleteUserSerializer(serializers.ModelSerializer):
    """Combined serializer for user with nested profile data"""
    profile = ProfileDataSerializer()  
    
    class Meta:
        model = User
        fields = '__all__' 
    
    def validate(self, data):
        return data
        
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Handle avatar field explicitly if it's present
        avatar = validated_data.get('avatar')
        if avatar is not None:
            instance.avatar = avatar
        
        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update or create UserProfile fields
        profile, created = UserProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        
        return instance

# Moved from account/serializers.py
class UserListSerializer(serializers.ModelSerializer):
    """Optimized serializer for user listing table view"""
    department = serializers.CharField(source='employee_profile.department', read_only=True, default='N/A')
    jobTitle = serializers.CharField(source='employee_profile.job_title', read_only=True, default='N/A')
    
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 
            'avatar', 'is_active', 'user_type',
            'department', 'jobTitle'
        )

# Moved from account/serializers.py
class AgentProfileSerializer(serializers.ModelSerializer):
    """Serializer for agent-specific profile data"""
    company_name = serializers.StringRelatedField(read_only=True)
    # Add a write-only field for the company ID
    company_name_id = serializers.PrimaryKeyRelatedField(
        source='company_name',
        queryset=django_apps.get_model('company', 'Company').objects.all(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = AgentProfile
        exclude = ('user',) # Exclude user to avoid redundancy

# Moved from account/serializers.py
class ClientProfileSerializer(serializers.ModelSerializer):
    """Serializer for client-specific profile data"""
    company_name = serializers.StringRelatedField(read_only=True)
    # Add a write-only field for the client ID
    company_name_id = serializers.PrimaryKeyRelatedField(
        source='company_name',
        queryset=django_apps.get_model('client', 'Client').objects.all(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = ClientProfile
        exclude = ('user',)

# Moved from account/serializers.py
class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer for employee-specific profile data"""
    company_name = serializers.StringRelatedField(read_only=True)
    reports_to = serializers.StringRelatedField(read_only=True)
    
    # Add write-only fields for the related objects
    company_name_id = serializers.PrimaryKeyRelatedField(
        source='company_name',
        queryset=django_apps.get_model('company', 'Company').objects.all(),
        write_only=True,
        required=False
    )
    reports_to_id = serializers.PrimaryKeyRelatedField(
        source='reports_to',
        queryset=User.objects.all(), # Keep this pointing to the shared User model
        write_only=True,
        required=False
    )
    
    class Meta:
        model = EmployeeProfile
        exclude = ('user',)

# Moved from account/serializers.py
class UserProfileAdminSerializer(serializers.ModelSerializer):
    """Comprehensive serializer for admin user profile management"""
    profile = ProfileDataSerializer(required=False)
    agent_profile = AgentProfileSerializer(required=False)
    client_profile = ClientProfileSerializer(required=False)
    employee_profile = EmployeeProfileSerializer(required=False)
    
    class Meta:
        model = User # Based on the shared User model
        fields = (
            'id', 'email', 'first_name', 'last_name', 
            'is_active', 'is_tenant_owner', 'date_joined', 'last_login',
            'profile', 
            'agent_profile', 'client_profile', 'employee_profile'
        )
    
    def update(self, instance, validated_data):
        # Pop related profile data
        profile_data = validated_data.pop('profile', {})
        agent_profile_data = validated_data.pop('agent_profile', {})
        client_profile_data = validated_data.pop('client_profile', {})
        employee_profile_data = validated_data.pop('employee_profile', {})
        
        # Update User fields first
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update or create UserProfile fields if data is provided
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        # Helper function to update or create specific profiles
        def update_or_create_specific_profile(ProfileModel, profile_data, required_fields=None):
            if not profile_data:
                return # Nothing to update

            try:
                specific_profile = ProfileModel.objects.get(user=instance)
                existing = True
            except ProfileModel.DoesNotExist:
                specific_profile = ProfileModel(user=instance)
                existing = False

            # Apply data
            for attr, value in profile_data.items():
                setattr(specific_profile, attr, value)

            # Validate required fields
            if required_fields:
                for field, error_msg in required_fields.items():
                    if not getattr(specific_profile, field, None):
                        raise serializers.ValidationError({
                            ProfileModel._meta.model_name.lower() + '_profile': {field: error_msg}
                        })

            try:
                specific_profile.save()
            except Exception as e:
                 if 'constraint' in str(e).lower():
                     field_errors = {}
                     if required_fields:
                         for field, error_msg in required_fields.items():
                            if field in str(e).lower():
                                field_errors[field] = error_msg
                     if not field_errors:
                        field_errors['_all_'] = f"Database constraint violation saving {ProfileModel._meta.verbose_name}."
                     raise serializers.ValidationError({
                         ProfileModel._meta.model_name.lower() + '_profile': field_errors
                     })
                 raise

        # Update/Create profiles if data is present
        if agent_profile_data:
            update_or_create_specific_profile(
                AgentProfile,
                agent_profile_data,
                required_fields={'company_name': 'Company name is required for agent profiles.'}
            )
        elif client_profile_data:
             update_or_create_specific_profile(
                 ClientProfile,
                 client_profile_data,
                 required_fields={'company_name': 'Company name is required for client profiles.'}
            )
        elif employee_profile_data:
            update_or_create_specific_profile(
                EmployeeProfile,
                employee_profile_data,
                required_fields={'company_name': 'Company name is required for employee profiles.'}
            )

        return instance 

