from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializerLogin, UserSerializerProfile

class CurrentUserLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializerLogin(request.user)
        return Response(serializer.data)

class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializerProfile(request.user)
        return Response(serializer.data)

