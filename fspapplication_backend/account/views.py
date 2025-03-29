from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import LoginUserSerializer, CompleteUserSerializer
from .models import UserProfile

class CurrentUserLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = LoginUserSerializer(request.user)
        return Response(serializer.data)

class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = CompleteUserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        serializer = CompleteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

