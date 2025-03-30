from rest_framework import generics, status
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer


class CompanyDetailView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the singleton company instance.
    """
    serializer_class = CompanySerializer
    
    def get_object(self):
        """
        Return the singleton company instance.
        """
        return Company.get_solo()
