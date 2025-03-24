from django.http import Http404
from django_tenants.middleware.main import TenantMainMiddleware

class CustomTenantMiddleware(TenantMainMiddleware):
    def get_tenant(self, model, hostname):
        # The base Django-Tenants code calls get_tenant(model, hostname),
        # so we must match that signature (no 'request' argument).
        try:
            return super().get_tenant(model, hostname)
        except Exception:
            # Instead of a server error (500), raise a 404
            raise Http404("❌ Invalid tenant or subdomain.")
