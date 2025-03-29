from rest_framework import serializers
from .models import User, UserProfile

class UserSerializerLogin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
        )
        read_only_fields = ('id',)
        
class UserSerializerProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'user_type',
            'first_name',
            'last_name',
            'avatar',
            'functional_groups',
            'is_active',
            'is_superuser',
            'is_staff',
            'date_joined',
            'last_login',   
        )
        model = UserProfile
        fields = (
            'id',
            'user',
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
            'date_of_birth',
            'created_at',
            'updated_at',
        )

