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
            'is_active',
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
        required=False,
        allow_null=True # Allow null when reading/writing if not required
    )
    # Explicitly define client_since to ensure null/blank is handled
    client_since = serializers.DateField(required=False, allow_null=True)
    
    class Meta:
        model = ClientProfile
        exclude = ('user',) # Exclude user to avoid redundancy

# Moved from account/serializers.py
class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer for employee-specific profile data"""
    # Company name is now read-only as it's set automatically by the model
    company_name = serializers.StringRelatedField(read_only=True)
    reports_to = serializers.StringRelatedField(read_only=True)
    
    # Remove company_name_id write field
    # company_name_id = serializers.PrimaryKeyRelatedField(...)
    
    # Keep reports_to_id if needed for setting the manager
    reports_to_id = serializers.PrimaryKeyRelatedField(
        source='reports_to',
        queryset=User.objects.all(), # Keep this pointing to the shared User model
        write_only=True,
        required=False,
        allow_null=True # Allow clearing the manager
    )
    
    class Meta:
        model = EmployeeProfile
        # Exclude user and the now redundant company_name_id
        exclude = ('user',)

# Moved from account/serializers.py
class UserProfileAdminSerializer(serializers.ModelSerializer):
    """Comprehensive serializer for admin user profile management"""
    profile = ProfileDataSerializer(required=False)
    # Explicitly mark nested profiles as not required for validation
    agent_profile = AgentProfileSerializer(required=False, allow_null=True)
    client_profile = ClientProfileSerializer(required=False, allow_null=True)
    employee_profile = EmployeeProfileSerializer(required=False, allow_null=True)
    
    class Meta:
        model = User # Based on the shared User model
        fields = (
            'id', 'email', 'first_name', 'last_name', 
            'is_active', 'is_tenant_owner', 'date_joined', 'last_login',
            'user_type',
            'profile', 
            'agent_profile', 'client_profile', 'employee_profile'
        )
    
    def update(self, instance, validated_data):
        print(f"[Serializer Update] Instance: {instance}, Validated Data: {validated_data}")

        # Pop related profile data - use None default to distinguish missing from empty {}
        profile_data = validated_data.pop('profile', None)
        agent_profile_data = validated_data.pop('agent_profile', None)
        client_profile_data = validated_data.pop('client_profile', None)
        employee_profile_data = validated_data.pop('employee_profile', None)
        
        # Determine the target user_type from validated_data
        new_user_type = validated_data.get('user_type', None)
        original_user_type = instance.user_type
        is_type_change = new_user_type is not None and new_user_type != original_user_type

        print(f"[Serializer Update] Original Type: {original_user_type}, New Type: {new_user_type}, Type Change: {is_type_change}")

        # If the type is changing, delete the old profile FIRST
        if is_type_change:
            print(f"[Serializer Update] Deleting profiles for old type: {original_user_type}")
            if original_user_type == 'agent' and hasattr(instance, 'agent_profile'):
                print("--> Deleting AgentProfile")
                instance.agent_profile.delete()
            elif original_user_type == 'client' and hasattr(instance, 'client_profile'):
                print("--> Deleting ClientProfile")
                instance.client_profile.delete()
            elif original_user_type == 'employee' and hasattr(instance, 'employee_profile'):
                print("--> Deleting EmployeeProfile")
                instance.employee_profile.delete()
        
        # Update User instance fields from validated_data (including user_type if changed)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Save the User instance *after* potential deletions and attribute updates
        print(f"[Serializer Update] Saving User instance: {instance.email}, New Type: {instance.user_type}")
        instance.save() 
        print("[Serializer Update] User instance saved.")

        # Update or create the main UserProfile if data was provided
        if profile_data is not None: # Check if 'profile' key was present
            print("[Serializer Update] Updating main UserProfile...")
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            print("[Serializer Update] Main UserProfile saved.")
            
        # Helper function remains the same
        def update_or_create_specific_profile(ProfileModel, profile_data, required_fields=None):
            # Only proceed if data is explicitly provided for this specific profile type
            if profile_data is None: 
                print(f"[Helper] No data provided for {ProfileModel.__name__}, skipping.")
                return

            print(f"[Helper] Updating/Creating {ProfileModel.__name__}...")
            profile_exists = True
            try:
                specific_profile = ProfileModel.objects.get(user=instance)
                print(f"--> Found existing {ProfileModel.__name__}")
            except ProfileModel.DoesNotExist:
                profile_exists = False
                # Check if we are creating AND the input data is empty
                if not profile_data:
                    print(f"--> Attempting to create {ProfileModel.__name__} with empty data. Skipping save.")
                    return # Don't create if data is empty {}
                specific_profile = ProfileModel(user=instance)
                print(f"--> Creating new {ProfileModel.__name__}")

            # Apply data
            for attr, value in profile_data.items():
                setattr(specific_profile, attr, value)

            # Validate required fields if necessary (only if creating or updating with non-empty data)
            if required_fields and profile_data:
                for field, error_msg in required_fields.items():
                    if not getattr(specific_profile, field, None):
                        print(f"[Helper] Validation Error: Missing required field '{field}' for {ProfileModel.__name__}")
                        raise serializers.ValidationError({
                            ProfileModel._meta.model_name.lower() + '_profile': {field: error_msg}
                        })
            elif not profile_exists and not profile_data:
                # This case is already handled by the check after DoesNotExist, but adding for clarity
                print(f"[Helper] Skipping validation and save for {ProfileModel.__name__} due to empty creation attempt.")
                return

            try:
                specific_profile.save()
                print(f"[Helper] Saved {ProfileModel.__name__}")
            except Exception as e:
                 print(f"[Helper] Error saving {ProfileModel.__name__}: {e}")
                 if 'constraint' in str(e).lower():
                     field_errors = {}
                     if required_fields:
                        for field, error_msg in required_fields.items():
                             if field in str(e).lower() or not getattr(specific_profile, field, None):
                                 field_errors[field] = error_msg
                     if not field_errors:
                        field_errors['_generic_'] = f"Database constraint error saving {ProfileModel._meta.verbose_name}. Please check required fields."
                     # Attach errors to the specific profile type field in the main serializer
                     raise serializers.ValidationError({
                         ProfileModel._meta.model_name.lower() + '_profile': field_errors
                     })
                 raise # Re-raise other exceptions

        # Update/Create specific profiles ONLY IF data for them was explicitly passed in the request
        # (which it won't be during a simple type change)
        final_user_type = instance.user_type # Use the type from the saved instance
        print(f"[Serializer Update] Final user type after save: {final_user_type}")
        print(f"[Serializer Update] Checking if specific profile data was provided:")
        print(f"--> Agent Data Provided: {agent_profile_data is not None}")
        print(f"--> Client Data Provided: {client_profile_data is not None}")
        print(f"--> Employee Data Provided: {employee_profile_data is not None}")

        # Only call the helper if the corresponding data dict was present in the request payload
        if agent_profile_data is not None:
            print("[Serializer Update] Processing provided AgentProfile data...")
            update_or_create_specific_profile(
                AgentProfile,
                agent_profile_data, 
                required_fields={'company_name': 'Company name is required for agent profiles.'}
            )
        
        if client_profile_data is not None:
             print("[Serializer Update] Processing provided ClientProfile data...")
             update_or_create_specific_profile(
                 ClientProfile,
                 client_profile_data,
                 required_fields={'company_name': 'Company name is required for client profiles.'}
            )
        
        if employee_profile_data is not None:
            print("[Serializer Update] Processing provided EmployeeProfile data...")
            update_or_create_specific_profile(
                EmployeeProfile,
                employee_profile_data,
                # No longer require company_name here, model handles it
                required_fields={}
            )

        print("[Serializer Update] Update method finished.")
        return instance 

