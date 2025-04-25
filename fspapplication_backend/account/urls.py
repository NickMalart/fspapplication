from django.urls import path
from .views import CurrentUserLoginView, CurrentUserProfileView, UserListView, UserProfileAdminView, FinalizeTenantAuthenticationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Define the app name if not already defined
app_name = 'account'

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', CurrentUserLoginView.as_view(), name='current-user'),
    path('profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('profile/update/', CurrentUserProfileView.as_view(), name='current-user-profile-update'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<uuid:pk>/', UserProfileAdminView.as_view(), name='user-profile-admin'),
    path('auth/finalize/', FinalizeTenantAuthenticationView.as_view(), name='auth_finalize_tenant'),
]