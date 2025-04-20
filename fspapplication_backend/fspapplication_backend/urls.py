from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.views.static import serve
import os

def health_check(request):
    return HttpResponse("OK")

def serve_vue_frontend(request, path=''):
    """
    Serve the Vue.js frontend files from the static directory
    If the file doesn't exist, serve the index.html file for client-side routing
    """
    if path and os.path.exists(os.path.join(settings.BASE_DIR, 'static', path)):
        return serve(request, path, document_root=os.path.join(settings.BASE_DIR, 'static'))
    return serve(request, 'index.html', document_root=os.path.join(settings.BASE_DIR, 'static'))

urlpatterns = [
    path('auth/', include('kinde_auth.urls')),
    path('api/account/', include('account.urls')),
    path('api/company/', include('company.urls')),
    path('api/files/', include('files.urls')),
    path('api/client/', include('client.urls')),
    path('api/agent/', include('agent.urls')),
    path('api/', include('common_utils.urls')),
    path('api/user-management/', include('user_management.urls')),
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('<path:path>', serve_vue_frontend),
    path('', serve_vue_frontend),
]
