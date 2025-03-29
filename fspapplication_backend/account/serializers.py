from rest_framework import serializers
from .models import User, UserProfile, EmployeeProfile, FunctionalGroup

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model with full CRUD operations"""
    full_address = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = (
            'id',
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
            'full_address'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_full_address(self, obj):
        """Returns a formatted full address string"""
        address_parts = []
        if obj.street_number and obj.street_name:
            address_parts.append(f"{obj.street_number} {obj.street_name}")
        if obj.suburb:
            address_parts.append(obj.suburb)
        if obj.city:
            address_parts.append(obj.city)
        if obj.state:
            address_parts.append(obj.state)
        if obj.postal_code:
            address_parts.append(obj.postal_code)
        if obj.country:
            address_parts.append(obj.country)
        return ", ".join(filter(None, address_parts))

    def validate_phone_number(self, value):
        """Validate phone number format"""
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Invalid phone number format")
        return value

    def validate_emergency_contact(self, value):
        """Validate emergency contact number format"""
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Invalid emergency contact number format")
        return value

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model with nested profile handling"""
    profile = UserProfileSerializer()
    full_name = serializers.SerializerMethodField()
    functional_groups = serializers.SerializerMethodField()
    specific_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'avatar',
            'user_type',
            'profile',
            'functional_groups',
            'specific_profile',
            'is_active',
            'date_joined',
            'last_login'
        )
        read_only_fields = ('id', 'date_joined', 'last_login')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_functional_groups(self, obj):
        return list(obj.functional_groups.values('id', 'name', 'code'))

    def get_specific_profile(self, obj):
        """Returns the specific profile based on user_type"""
        profile = obj.get_specific_profile()
        if profile:
            if obj.is_employee:
                from organisation.serializers import CompanySerializer
                return {
                    'type': 'employee',
                    'company': CompanySerializer(profile.company).data,
                    'department': profile.department,
                    'employee_id': profile.employee_id,
                    'job_title': profile.job_title,
                    'start_date': profile.start_date
                }
            elif obj.is_agent:
                return {
                    'type': 'agent',
                    'company_name': profile.company_name,
                    'license_number': profile.license_number,
                    'years_of_experience': profile.years_of_experience
                }
            elif obj.is_client:
                return {
                    'type': 'client',
                    'company_name': profile.company_name,
                    'industry': profile.industry,
                    'client_since': profile.client_since
                }
        return None

    def create(self, validated_data):
        """Create a new user with nested profile data"""
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create(**validated_data)
        
        # Profile will be created by signal, we just need to update it
        if profile_data:
            for attr, value in profile_data.items():
                setattr(user.profile, attr, value)
            user.profile.save()
        
        return user

    def update(self, instance, validated_data):
        """Update user and nested profile data"""
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

    def validate_email(self, value):
        """Validate email format and uniqueness"""
        if User.objects.exclude(pk=self.instance.pk if self.instance else None).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value.lower()

    def validate(self, data):
        """Additional validation for the entire object"""
        if 'first_name' in data and 'last_name' in data:
            if not (data['first_name'] or data['last_name']):
                raise serializers.ValidationError("Either first name or last name must be provided")
        return data

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
