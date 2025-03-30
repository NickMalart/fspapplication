from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import logging
from .models import Company
from .serializers import CompanySerializer

logger = logging.getLogger(__name__)

class CompanyView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        company = Company.get_solo()
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    
    def put(self, request):
        logger.info(f"Updating company information")
        logger.debug(f"Request data: {request.data}")
        
        company = Company.get_solo()
        
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            logger.info("Serializer validation passed")
            try:
                company = serializer.save()
                logger.info(f"Company updated successfully: {company.id}")
                return Response(serializer.data)
            except Exception as e:
                logger.error(f"Error saving company: {str(e)}")
                return Response({"error": str(e)}, status=500)
        else:
            logger.error(f"Serializer validation failed: {serializer.errors}")
            return Response(serializer.errors, status=400)