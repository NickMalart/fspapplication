from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')), 
    path('api/common_utils/', include('common_utils.urls')),
    path('api/client/', include('client.urls')),
] 