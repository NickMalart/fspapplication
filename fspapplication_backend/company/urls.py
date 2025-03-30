from django.urls import path
from .views import CompanyDetailView

app_name = 'company'

urlpatterns = [
    path('', CompanyDetailView.as_view(), name='company-detail'),
]
