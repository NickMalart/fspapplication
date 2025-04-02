from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client
from .serializers import ClientSerializer

# Add pagination class
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ClientListView(generics.ListAPIView):
    """API view to list all clients with filtering, sorting and pagination"""
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'business_name', 'email', 'phone']
    ordering_fields = [
        'name', 'business_name', 'email', 'industry', 'city', 
        'state', 'country', 'is_active', 'created_at'
    ]
    ordering = ['name']
    
    def get_queryset(self):
        queryset = Client.objects.all()
        
        # Status filter (active, inactive, all)
        status = self.request.query_params.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Search for client by name, business name, or email
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(business_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
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
