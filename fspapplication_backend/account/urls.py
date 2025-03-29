from django.urls import path
from .views import CurrentUserLoginView, CurrentUserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', CurrentUserLoginView.as_view(), name='current-user'),
    path('user/profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('user/profile/update/', CurrentUserProfileView.as_view(), name='current-user-profile-update'),
]