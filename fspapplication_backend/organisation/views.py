from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(viewsets.ViewSet):
    def retrieve(self, request):
        company = Company.get_solo()
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def update(self, request):
        company = Company.get_solo()
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)