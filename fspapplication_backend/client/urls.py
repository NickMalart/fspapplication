from django.urls import path
from .views import (
    ClientListView, 
    ClientDetailView,
    ClientContractListView,
    ClientContractDetailView
)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<uuid:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/<uuid:client_id>/contracts/', ClientContractListView.as_view(), name='client-contract-list'),
    path('clients/<uuid:client_id>/contracts/<uuid:pk>/', ClientContractDetailView.as_view(), name='client-contract-detail'),
]

# Add format suffix support for API endpoints (like .json)
urlpatterns = format_suffix_patterns(urlpatterns) 