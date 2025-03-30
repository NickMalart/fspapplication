from rest_framework import generics, status
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer


class CompanyDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CompanySerializer
    
    def get_object(self):
        return Company.get_solo()
