from django.urls import path
from .views import (
    AgentListView, 
    AgentDetailView,
    AgentWarehouseListView,
    AgentWarehouseDetailView
)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('agents/', AgentListView.as_view(), name='agent-list'),
    path('agents/<uuid:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('agents/<uuid:agent_id>/warehouses/', AgentWarehouseListView.as_view(), name='agent-warehouse-list'),
    path('agents/<uuid:agent_id>/warehouses/<uuid:pk>/', AgentWarehouseDetailView.as_view(), name='agent-warehouse-detail'),
]

# Add format suffix support for API endpoints (like .json)
urlpatterns = format_suffix_patterns(urlpatterns) 