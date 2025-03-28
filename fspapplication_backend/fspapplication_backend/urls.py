from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/account/', include('account.urls')),
    path('api/organisation/', include('organisation.urls')),
    path('admin/', admin.site.urls),
]
