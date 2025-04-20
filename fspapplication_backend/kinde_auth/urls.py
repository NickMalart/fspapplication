# fspapplication_backend/auth/urls.py
from django.urls import path
from . import views

app_name = 'kinde_auth' # Use the unique app label

urlpatterns = [
    path('callback/', views.KindeCallbackView.as_view(), name='kinde_callback'),
    # Add login and logout URLs later
    # path('login/', views.KindeLoginView.as_view(), name='kinde_login'),
    # path('logout/', views.KindeLogoutView.as_view(), name='kinde_logout'),
] 