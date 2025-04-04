from rest_framework import serializers
from django.apps import apps as models
from .models import User, UserProfile, FunctionalGroup, AgentProfile, ClientProfile, EmployeeProfile

class LoginUserSerializer(serializers.ModelSerializer):
    """Serializer for basic user login information"""
    class Meta:
        model = User
        fields = ('id', 'email')
        read_only_fields = ('id',)

class ProfileDataSerializer(serializers.ModelSerializer):
    """Serializer for user profile data only"""
    class Meta:
        model = UserProfile
        exclude = ('user',) 

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

class FunctionalGroupSerializer(serializers.ModelSerializer):
    """Serializer for functional groups"""
    class Meta:
        model = FunctionalGroup
        fields = ('id', 'code', 'name', 'color')

class AgentProfileSerializer(serializers.ModelSerializer):
    """Serializer for agent-specific profile data"""
    company_name = serializers.StringRelatedField(read_only=True)
    # Add a write-only field for the company ID
    company_name_id = serializers.PrimaryKeyRelatedField(
        source='company_name',
        queryset=models.get_model('company', 'Company').objects.all(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = AgentProfile
        exclude = ('user',)

class ClientProfileSerializer(serializers.ModelSerializer):
    """Serializer for client-specific profile data"""
    company_name = serializers.StringRelatedField(read_only=True)
    # Add a write-only field for the client ID
    company_name_id = serializers.PrimaryKeyRelatedField(
        source='company_name',
        queryset=models.get_model('client', 'Client').objects.all(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = ClientProfile
        exclude = ('user',)

class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer for employee-specific profile data"""
    company_name = serializers.StringRelatedField(read_only=True)
    reports_to = serializers.StringRelatedField(read_only=True)
    
    # Add write-only fields for the related objects
    company_name_id = serializers.PrimaryKeyRelatedField(
        source='company_name',
        queryset=models.get_model('company', 'Company').objects.all(),
        write_only=True,
        required=False
    )
    reports_to_id = serializers.PrimaryKeyRelatedField(
        source='reports_to',
        queryset=User.objects.all(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = EmployeeProfile
        exclude = ('user',)

class UserProfileAdminSerializer(serializers.ModelSerializer):
    """Comprehensive serializer for admin user profile management"""
    profile = ProfileDataSerializer(required=False)
    functional_groups = FunctionalGroupSerializer(many=True, read_only=True)
    agent_profile = AgentProfileSerializer(required=False)
    client_profile = ClientProfileSerializer(required=False)
    employee_profile = EmployeeProfileSerializer(required=False)
    
    # IDs for managing functional groups (write operations)
    functional_group_ids = serializers.PrimaryKeyRelatedField(
        source='functional_groups',
        queryset=FunctionalGroup.objects.all(),
        many=True,
        required=False,
        write_only=True
    )
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'avatar', 
            'user_type', 'is_active', 'is_tenant_owner', 'date_joined', 'last_login',
            'profile', 'functional_groups', 'functional_group_ids',
            'agent_profile', 'client_profile', 'employee_profile'
        )
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        agent_profile_data = validated_data.pop('agent_profile', {})
        client_profile_data = validated_data.pop('client_profile', {})
        employee_profile_data = validated_data.pop('employee_profile', {})
        
        # Handle functional groups if present
        if 'functional_groups' in validated_data:
            instance.functional_groups.set(validated_data.pop('functional_groups'))
        
        # Check if user_type is being updated and handle profile type transitions
        original_user_type = instance.user_type
        new_user_type = validated_data.get('user_type', original_user_type)
        user_type_changed = new_user_type != original_user_type
        
        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update or create UserProfile fields
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        # Clear ALL profile data if user type changed - no data should be left behind
        if user_type_changed:
            # Always delete all specific profiles when type changes
            AgentProfile.objects.filter(user=instance).delete()
            ClientProfile.objects.filter(user=instance).delete()
            EmployeeProfile.objects.filter(user=instance).delete()
        
        # Update or create AgentProfile only if user is an agent
        if new_user_type == User.USER_TYPE_AGENT and agent_profile_data:
            agent_profile, created = AgentProfile.objects.get_or_create(user=instance)
            
            # Skip validation if we're just changing the user type
            skip_validation = user_type_changed
                
            # Only validate company_name for non-type-change updates
            if not skip_validation and 'company_name' not in agent_profile_data and created:
                raise serializers.ValidationError({
                    'agent_profile': {'company_name': 'This field is required when creating an agent profile.'}
                })
            
            for attr, value in agent_profile_data.items():
                setattr(agent_profile, attr, value)
            
            # Only save if not a user type change or if required fields are present
            if not user_type_changed or 'company_name' in agent_profile_data:
                agent_profile.save()
        
        # Update or create ClientProfile only if user is a client
        if new_user_type == User.USER_TYPE_CLIENT and client_profile_data:
            client_profile, created = ClientProfile.objects.get_or_create(user=instance)
            
            # Skip validation if we're just changing the user type
            skip_validation = user_type_changed
                
            # Only validate company_name for non-type-change updates
            if not skip_validation and 'company_name' not in client_profile_data and created:
                raise serializers.ValidationError({
                    'client_profile': {'company_name': 'This field is required when creating a client profile.'}
                })
            
            for attr, value in client_profile_data.items():
                setattr(client_profile, attr, value)
            
            # Always save client profile as string fields can be empty
            client_profile.save()
        
        # Update or create EmployeeProfile only if user is an employee
        if new_user_type == User.USER_TYPE_EMPLOYEE and employee_profile_data:
            employee_profile, created = EmployeeProfile.objects.get_or_create(user=instance)
            
            # Skip validation if we're just changing the user type
            skip_validation = user_type_changed
                
            # Only validate required fields for non-type-change updates
            if not skip_validation and created:
                required_fields = ['company_name', 'department']
                missing_fields = [field for field in required_fields if field not in employee_profile_data]
                if missing_fields:
                    raise serializers.ValidationError({
                        'employee_profile': {field: f'This field is required when creating an employee profile.' 
                                          for field in missing_fields}
                    })
            
            for attr, value in employee_profile_data.items():
                setattr(employee_profile, attr, value)
            
            # Only save if not a user type change or if required fields are present
            if not user_type_changed or ('company_name' in employee_profile_data and 'department' in employee_profile_data):
                employee_profile.save()
        
        return instance

