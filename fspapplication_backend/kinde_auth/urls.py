# fspapplication_backend/auth/urls.py
from django.urls import path
from .views import KindeLoginView, KindeCallbackView, KindeLogoutView

app_name = 'kinde_auth' # Use the unique app label

urlpatterns = [
    path('login/', KindeLoginView.as_view(), name='kinde_login'),
    path('callback/', KindeCallbackView.as_view(), name='kinde_callback'),
    path('logout/', KindeLogoutView.as_view(), name='kinde_logout'),
] 