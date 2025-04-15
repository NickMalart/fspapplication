from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer


class CompanyDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return Company.get_solo()
