from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import LoginUserSerializer, CompleteUserSerializer
from .models import UserProfile, User

# Add pagination class
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CurrentUserLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = LoginUserSerializer(request.user)
        return Response(serializer.data)

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

class UserListView(generics.ListAPIView):
    """API view to list all users with filtering, sorting and pagination"""
    serializer_class = CompleteUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = [
        'first_name', 'last_name', 'email', 'is_active', 'user_type',
        'employee_profile__job_title', 'employee_profile__department'
    ]
    ordering = ['first_name']  # Default sorting
    
    def get_queryset(self):
        queryset = User.objects.all().select_related(
            'profile', 'employee_profile', 'agent_profile', 'client_profile'
        )
        
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
            ordering = ordering.replace('.', '__')
            
            return f"{desc_prefix}{ordering}"
        
        return super().get_ordering()

