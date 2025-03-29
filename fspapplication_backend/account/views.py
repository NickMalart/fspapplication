from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    UserSerializer, 
    UserListSerializer, 
    UserProfileSerializer
)
from .models import User, UserProfile

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size = 10  # Default page size

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Comprehensive search across multiple fields
    search_fields = [
        'first_name', 
        'last_name', 
        'email', 
        'employee_profile__department', 
        'employee_profile__job_title',
        'user_type'
    ]
    
    # Allow filtering and ordering on multiple fields
    filterset_fields = ['user_type', 'is_active']
    ordering_fields = [
        'first_name', 
        'last_name', 
        'email', 
        'date_joined', 
        'employee_profile__department', 
        'employee_profile__job_title'
    ]

    def get_queryset(self):
        """
        This view should return a list of all users
        for the currently authenticated user.
        """
        queryset = User.objects.select_related(
            'profile', 
            'employee_profile__company'
        ).prefetch_related('functional_groups')
        
        # Handle status filtering
        status = self.request.query_params.get('status', 'active')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action
        """
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """
        Create a new user instance.
        Add any additional logic needed when creating a user.
        """
        user = serializer.save()
        # Add any post-save operations here if needed

    def perform_update(self, serializer):
        """
        Update a user instance.
        Add any additional logic needed when updating a user.
        """
        user = serializer.save()
        # Add any post-update operations here if needed

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """
        Retrieve user profile details
        """
        user = self.get_object()
        serializer = UserProfileSerializer(user.profile)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_profile(self, request, pk=None):
        """
        Update user profile details
        """
        user = self.get_object()
        serializer = UserProfileSerializer(user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a user
        """
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'user activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a user
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'user deactivated'})

class CurrentUserView(APIView):
    """
    View to handle current user operations
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        """
        Retrieve current user details
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """
        Update current user details
        """
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user profile instances.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.select_related('user')

    def get_queryset(self):
        """
        This view should return a list of all profiles
        for the currently authenticated user.
        """
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """
        Get the profile of the current user
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_my_profile(self, request):
        """
        Update the profile of the current user
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)