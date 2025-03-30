from rest_framework import serializers
from .models import User, UserProfile

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

