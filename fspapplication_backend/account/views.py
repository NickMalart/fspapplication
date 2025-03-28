from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, UserListSerializer
from rest_framework import generics
from .models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserListView(generics.ListAPIView):
    queryset = User.objects.select_related('employee_profile__company').prefetch_related('functional_groups')
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Default to only active users
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', 'active')
        
        if status == 'active':
            return queryset.filter(is_active=True)
        elif status == 'inactive':
            return queryset.filter(is_active=False)
        
        return queryset

    filterset_fields = ['user_type']
    search_fields = ['first_name', 'last_name', 'email', 'employee_profile__department', 'employee_profile__job_title']
    ordering_fields = ['first_name', 'last_name', 'date_joined', 'employee_profile__start_date']