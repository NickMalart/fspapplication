from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, UserListSerializer
from rest_framework import generics, filters
from .models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size = 10  # Default page size

    def get_paginated_response(self, data):
        # Ensure consistent response even with zero entries
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })

class UserListView(generics.ListAPIView):
    queryset = User.objects.select_related('employee_profile__company').prefetch_related('functional_groups')
    serializer_class = UserListSerializer
    pagination_class = CustomPageNumberPagination
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
        queryset = super().get_queryset()
        
        # Handle status filtering
        status = self.request.query_params.get('status', 'active')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        return queryset

class CurrentUserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def patch(self, request):
        """
        Partially update the current user's profile
        Supports updating user and user profile information
        Allows both JSON data and file uploads
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)