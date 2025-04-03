from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client, ClientContract
from .serializers import ClientSerializer, ClientContractSerializer

# Add pagination class
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ClientListView(generics.ListCreateAPIView):
    """API view to list and create clients with filtering, sorting and pagination"""
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'phone', 'abn']
    ordering_fields = [
        'name', 'email', 'abn', 'city', 
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
        
        # Search for client by name, email, or phone
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(abn__icontains=search)
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


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a single client by ID"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientContractListView(generics.ListCreateAPIView):
    """API view to list and create client contracts with filtering, sorting and pagination"""
    serializer_class = ClientContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'is_active', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = ClientContract.objects.all()
        
        # Filter by client
        client_id = self.request.query_params.get('client')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        
        # Status filter (active, inactive, all)
        status = self.request.query_params.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Search for contract by name or description
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
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

class ClientContractDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a single client contract by ID"""
    queryset = ClientContract.objects.all()
    serializer_class = ClientContractSerializer
    permission_classes = [permissions.IsAuthenticated]
