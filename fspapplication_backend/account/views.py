from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import LoginUserSerializer, CompleteUserSerializer
from .models import UserProfile
import logging

logger = logging.getLogger(__name__)

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
        logger.info(f"Updating user profile for {request.user.email}")
        logger.debug(f"Request data: {request.data}")
        
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        serializer = CompleteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            logger.info("Serializer validation passed")
            try:
                user = serializer.save()
                logger.info(f"User profile updated successfully: {user.id}")
                return Response(serializer.data)
            except Exception as e:
                logger.error(f"Error saving user profile: {str(e)}")
                return Response({"error": str(e)}, status=500)
        else:
            logger.error(f"Serializer validation failed: {serializer.errors}")
            return Response(serializer.errors, status=400)

