from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CurrentUserView, UserViewSet, UserProfileViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    # JWT Authentication endpoints
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Current user endpoints
    path('me/', CurrentUserView.as_view(), name='current-user'),
    
    # Include the router URLs
    path('', include(router.urls)),
]