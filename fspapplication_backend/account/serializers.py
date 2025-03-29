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
        exclude = ('user',)  # Exclude the user field to avoid recursion

class CompleteUserSerializer(serializers.ModelSerializer):
    """Combined serializer for user with nested profile data"""
    profile = ProfileDataSerializer()  
    
    class Meta:
        model = User
        fields = '__all__'  # Include all User fields + the profile field
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
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

