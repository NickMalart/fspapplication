from django.urls import path
from .views import CurrentUserView, UserListView, CurrentUserUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', CurrentUserView.as_view(), name='current-user'),
    path('user/update/', CurrentUserUpdateView.as_view(), name='update-current-user'),
    path('users/', UserListView.as_view(), name='user-list'),
]