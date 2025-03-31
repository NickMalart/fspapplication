from rest_framework import serializers
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
    company_name = serializers.StringRelatedField()
    
    class Meta:
        model = AgentProfile
        exclude = ('user',)

class ClientProfileSerializer(serializers.ModelSerializer):
    """Serializer for client-specific profile data"""
    class Meta:
        model = ClientProfile
        exclude = ('user',)

class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer for employee-specific profile data"""
    company_name = serializers.StringRelatedField()
    reports_to = serializers.StringRelatedField()
    
    class Meta:
        model = EmployeeProfile
        exclude = ('user',)

class UserProfileAdminSerializer(serializers.ModelSerializer):
    """Comprehensive serializer for admin user profile management"""
    profile = ProfileDataSerializer(required=False)
    functional_groups = FunctionalGroupSerializer(many=True, read_only=True)
    agent_profile = AgentProfileSerializer(read_only=True, required=False)
    client_profile = ClientProfileSerializer(read_only=True, required=False)
    employee_profile = EmployeeProfileSerializer(read_only=True, required=False)
    
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
        
        # Handle functional groups if present
        if 'functional_groups' in validated_data:
            instance.functional_groups.set(validated_data.pop('functional_groups'))
        
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
        
        return instance

