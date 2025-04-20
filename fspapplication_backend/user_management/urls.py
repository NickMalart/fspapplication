from django.urls import path
from .views import CurrentUserProfileView, UserListView, UserProfileAdminView

# URLs moved from account/urls.py
urlpatterns = [
    path('profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('profile/update/', CurrentUserProfileView.as_view(), name='current-user-profile-update'),
    path('users/', UserListView.as_view(), name='user-list'), # Added name
    path('users/<uuid:pk>/', UserProfileAdminView.as_view(), name='user-profile-admin'),
] 