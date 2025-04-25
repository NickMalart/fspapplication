from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import LoginUserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CompleteUserSerializer, UserListSerializer, UserProfileAdminSerializer # Import from local serializers
from .models import UserProfile # Import from local models
from django.core.signing import Signer, BadSignature, SignatureExpired
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import connection # Import connection
import json # Import json
# Assuming you have a utility to get the current tenant schema name, if not provided by middleware
# from your_tenant_utils import get_current_tenant_schema_name

class CurrentUserLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = LoginUserSerializer(request.user)
        return Response(serializer.data)



# Moved from account/views.py
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Moved from account/views.py
class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = CompleteUserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        serializer = CompleteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

# Moved from account/views.py
class UserListView(generics.ListAPIView):
    """API view to list all users with filtering, sorting and pagination"""
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = [
        'first_name', 'last_name', 'email', 'is_active', 'user_type',
        'employee_profile__job_title', 'employee_profile__department' # Assuming employee_profile is accessible via User
    ]
    ordering = ['first_name']
    
    def get_queryset(self):
        # Need to ensure User model is fetched correctly, likely from account.models
        # Adjust related field access if necessary (e.g., EmployeeProfile might be in .models)
        queryset = User.objects.all().select_related('employee_profile') # Check if employee_profile relation needs update
        
        # Status filter (active, inactive, all)
        status = self.request.query_params.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Search for user by name or email
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
            
        return queryset
        
    def get_ordering(self):
        """
        Handle dot notation in field names and convert to Django's double-underscore notation
        """
        ordering = self.request.query_params.get('ordering')
        if ordering:
            # Handle descending prefix
            desc_prefix = ''
            if ordering.startswith('-'):
                desc_prefix = '-'
                ordering = ordering[1:]
            
            # Convert dot notation to double underscore
            # Adjust if related fields changed (e.g., 'employee_profile.job_title' -> 'employee_profile__job_title')
            ordering = ordering.replace('.', '__') 
            
            return f"{desc_prefix}{ordering}"
        
        return super().get_ordering()

# Moved from account/views.py
class UserProfileAdminView(APIView):
    """
    API view for admin users to view and update detailed user profile information.
    Requires admin permissions.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        """Get a specific user's detailed profile"""
        try:
            user = User.objects.get(pk=pk) # Use shared User model
            serializer = UserProfileAdminSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, pk=None):
        """Update a specific user's profile"""
        try:
            user = User.objects.get(pk=pk)
            # Use the UserProfileAdminSerializer from this app's serializers
            serializer = UserProfileAdminSerializer(user, data=request.data, partial=True)
            
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data)
                except Exception as e:
                    # This error handling might need adjustment based on model locations
                    if 'violates not-null constraint' in str(e):
                        # Extract the field name from error message
                        field_name = None
                        if 'company_name_id' in str(e):
                            field_name = 'company_name'
                        elif 'department' in str(e):
                            field_name = 'department'
                        
                        # Determine which profile has the issue
                        profile_type = None
                        # Check the actual model names/tables now within the account app
                        if 'account_clientprofile' in str(e): # Adjusted table name
                            profile_type = 'client_profile'
                        elif 'account_agentprofile' in str(e): # Adjusted table name
                            profile_type = 'agent_profile'
                        elif 'account_employeeprofile' in str(e): # Adjusted table name
                            profile_type = 'employee_profile'
                        
                        if profile_type and field_name:
                            return Response({
                                profile_type: {
                                    field_name: f"This field is required for this profile type."
                                }
                            }, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Re-raise the exception for any other errors
                    return Response({
                        "detail": f"Database error: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request, pk=None):
        """Partial update of a specific user's profile"""
        return self.put(request, pk)

# IMPORTANT: Ensure the key used here matches the key used when CREATING the temp_token
# It might be settings.SECRET_KEY or a dedicated key.
# Consider using TimestampSigner for expiration handling.
signer = Signer() 

class FinalizeTenantAuthenticationView(APIView):
    """
    Finalizes authentication on the tenant domain using a temporary token.
    Validates the token, finds the user within the tenant context,
    and issues final JWT tokens.
    """
    authentication_classes = [] # No authentication needed for this endpoint itself
    permission_classes = [] # Public endpoint

    def get(self, request, *args, **kwargs):
        temp_token = request.query_params.get('token')

        if not temp_token:
            return Response({'error': 'Temporary token missing.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Validate the temporary token and parse payload
            print(f"---> Attempting to unsign token: {temp_token[:20]}...")
            payload_str = signer.unsign(temp_token)
            print(f"---> Unsigned payload string: {payload_str}")
            
            try:
                payload = json.loads(payload_str)
                user_email = payload.get('email')
                if not user_email:
                    print("ERROR: 'email' not found in token payload.")
                    return Response({'error': 'Invalid token payload structure.'}, status=status.HTTP_400_BAD_REQUEST)
                print(f"---> Extracted email from payload: {user_email}")
            except json.JSONDecodeError:
                print(f"ERROR: Failed to decode JSON payload: {payload_str}")
                return Response({'error': 'Invalid token payload format.'}, status=status.HTTP_400_BAD_REQUEST)

            # 2. Get current tenant (Django Tenants middleware should provide this)
            tenant = getattr(request, 'tenant', None)
            if not tenant:
                 print("ERROR: Tenant context missing in FinalizeTenantAuthenticationView")
                 return Response({'error': 'Tenant context missing.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            print(f"---> Tenant identified: {tenant.schema_name}")
            print(f"---> DB Connection Schema BEFORE query: {connection.schema_name}")
            if connection.schema_name != tenant.schema_name:
                print(f"ERROR: DB connection schema '{connection.schema_name}' does NOT match tenant schema '{tenant.schema_name}'!")
                return Response({'error': 'Database schema mismatch detected.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # 3. Find the user within the tenant context using the extracted email
            try:
                print(f"---> Looking for user with email: {user_email} in schema: {connection.schema_name}")
                user = User.objects.get(email=user_email)
                print(f"---> Found user: {user.pk}")
            except User.DoesNotExist:
                print(f"User not found for email: {user_email} in tenant {tenant.schema_name}")
                return Response({'error': 'User not found for this tenant.'}, status=status.HTTP_404_NOT_FOUND)

            # 4. Generate final JWT tokens
            refresh = RefreshToken.for_user(user)
            # Optional: Add custom claims to the access token if needed
            # access_token = refresh.access_token
            # access_token['tenant_schema'] = tenant.schema_name

            response_data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    # Use user.pk or user.id depending on your model primary key type
                    'id': str(user.pk), 
                    'email': user.email,
                    # Add other non-sensitive user details if needed (e.g., first_name, last_name)
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tenant_schema_name': tenant.schema_name,
            }
            print(f"Finalization successful for user {user.email} in tenant {tenant.schema_name}") # Add logging
            return Response(response_data, status=status.HTTP_200_OK)

        except SignatureExpired:
            print(f"Temporary token expired: {temp_token[:20]}...") # Add logging
            return Response({'error': 'Temporary token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            print(f"Invalid temporary token signature: {temp_token[:20]}...") # Add logging
            return Response({'error': 'Invalid temporary token signature.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error during finalization: {e}")
            # Also log the schema name when the error occurs
            print(f"---> DB Connection Schema DURING exception: {connection.schema_name}") 
            return Response({'error': 'An unexpected error occurred during finalization.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


