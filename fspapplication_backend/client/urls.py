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
    path('contracts/', ClientContractListView.as_view(), name='contract-list'),
    path('contracts/<uuid:pk>/', ClientContractDetailView.as_view(), name='contract-detail'),
]

# Add format suffix support for API endpoints (like .json)
urlpatterns = format_suffix_patterns(urlpatterns) 