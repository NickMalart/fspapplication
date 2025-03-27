from django.http import Http404
from django_tenants.middleware.main import TenantMainMiddleware
import logging
from django.db import connection
from django.apps import apps

logger = logging.getLogger(__name__)

class CustomTenantMiddleware(TenantMainMiddleware):
    def get_tenant_model(self):
        """Get the tenant model from settings"""
        from django.conf import settings
        return apps.get_model(settings.TENANT_MODEL)
        
    def get_tenant_domain_model(self):
        """Get the tenant domain model from settings"""
        from django.conf import settings
        return apps.get_model(settings.TENANT_DOMAIN_MODEL)
        
    def process_request(self, request):
        # Check for tenant header first
        tenant_from_header = request.headers.get('X-DTS-TENANT')
        
        if tenant_from_header:
            logger.info(f"Tenant from header: {tenant_from_header}")
            # Get tenant model outside the try block to avoid UnboundLocalError
            tenant_model = self.get_tenant_model()
            
            try:
                # Get tenant by schema_name from header
                tenant = tenant_model.objects.get(schema_name=tenant_from_header)
                
                # Set tenant for this request
                connection.set_tenant(tenant)
                request.tenant = tenant
                
                logger.info(f"Successfully set tenant from header: {tenant.schema_name}")
                return None
            except tenant_model.DoesNotExist:
                logger.error(f"Tenant from header not found: {tenant_from_header}")
                raise Http404(f"❌ Invalid tenant header: {tenant_from_header}")
            except Exception as e:
                logger.error(f"Error processing tenant header: {str(e)}")
                # Fall through to domain-based resolution
        
        # If no header or header processing failed, fallback to domain-based tenant
        logger.info("Using domain-based tenant resolution")
        return super().process_request(request)
    
    def get_tenant(self, model, hostname):
        """Get tenant by hostname/domain"""
        try:
            # Extract subdomain from hostname
            hostname_parts = hostname.split('.')
            subdomain = hostname_parts[0] if len(hostname_parts) > 1 else None
            
            logger.info(f"Getting tenant for hostname: {hostname}, subdomain: {subdomain}")
            
            # First try to get tenant by domain
            domain = self.get_tenant_domain_model().objects.get(domain=hostname)
            return domain.tenant
        except self.get_tenant_domain_model().DoesNotExist:
            try:
                # If domain lookup fails, try by schema_name (assuming subdomain == schema_name)
                if subdomain and subdomain != 'localhost':
                    logger.info(f"Trying to get tenant by schema_name: {subdomain}")
                    return model.objects.get(schema_name=subdomain)
                else:
                    raise model.DoesNotExist("No valid subdomain")
            except model.DoesNotExist as e:
                logger.error(f"Tenant error: {str(e)}")
                raise Http404(f"❌ Invalid tenant. No tenant for hostname '{hostname}'")
    
    def activate_tenant(self, tenant, connection_obj=None):
        """Activate the tenant schema in the database connection"""
        # Use the provided connection or the default one
        from django.db import connection as default_connection
        conn = connection_obj or default_connection
        conn.set_tenant(tenant)
        logger.info(f"Activated tenant: {tenant.schema_name}")
