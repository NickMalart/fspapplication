from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/account/', include('account.urls')),
    path('api/company/', include('company.urls')),
    path('api/files/', include('files.urls')),
    path('api/client/', include('client.urls')),
    path('api/agent/', include('agent.urls')),
    path('', include('common_utils.urls')),
    path('admin/', admin.site.urls),
]
