from django.urls import path
from .views import CompanyAPIView

app_name = 'organisation'

urlpatterns = [
    path('company/', CompanyAPIView.as_view(), name='company'),
] 