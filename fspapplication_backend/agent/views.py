from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Agent, AgentWarehouse
from .serializers import AgentSerializer, AgentWarehouseSerializer

# Add pagination class
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AgentListView(generics.ListCreateAPIView):
    """API view to list and create agents with filtering, sorting and pagination"""
    serializer_class = AgentSerializer
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
        queryset = Agent.objects.all()
        
        # Status filter (active, inactive, all)
        status = self.request.query_params.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Search for agent by name, email, or phone
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


class AgentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a single agent by ID"""
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]


class AgentWarehouseListView(generics.ListCreateAPIView):
    """API view to list and create agent warehouses with filtering, sorting and pagination"""
    serializer_class = AgentWarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'city', 'state', 'country']
    ordering_fields = ['name', 'city', 'state', 'country', 'is_primary', 'is_active', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = AgentWarehouse.objects.all()
        
        # Get agent_id from URL parameters
        agent_id = self.kwargs.get('agent_id')
        if agent_id:
            queryset = queryset.filter(agent_id=agent_id)
        
        # Status filter (active, inactive, all)
        status = self.request.query_params.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Search for warehouse by name, description, or location
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(city__icontains=search) |
                Q(state__icontains=search) |
                Q(country__icontains=search)
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


class AgentWarehouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a single agent warehouse by ID"""
    queryset = AgentWarehouse.objects.all()
    serializer_class = AgentWarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]
