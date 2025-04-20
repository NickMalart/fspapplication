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


