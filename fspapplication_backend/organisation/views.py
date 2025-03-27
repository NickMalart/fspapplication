from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer

# Create your views here.

class CompanyAPIView(APIView):
    """
    API view to get company information.
    GET: Retrieve the company details (available to all authenticated users)
    PUT: Update company details (available only to admin users)
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get the company information"""
        company = Company.get_solo()
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    
    def put(self, request):
        """Update the company information (admin only)"""
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        company = Company.get_solo()
        serializer = CompanySerializer(company, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
