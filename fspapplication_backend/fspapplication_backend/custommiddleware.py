from django.http import Http404
from django_tenants.middleware.main import TenantMainMiddleware
import logging
from django.db import connection
from django.apps import apps
from functools import lru_cache

logger = logging.getLogger(__name__)

class CustomTenantMiddleware(TenantMainMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # In-memory cache for tenant resolution
        self._tenant_cache = {}
        
    def get_tenant_model(self):
        """Get the tenant model from settings"""
        from django.conf import settings
        return apps.get_model(settings.TENANT_MODEL)
        
    def get_tenant_domain_model(self):
        """Get the tenant domain model from settings"""
        from django.conf import settings
        return apps.get_model(settings.TENANT_DOMAIN_MODEL)
    
    @lru_cache(maxsize=32)
    def _get_tenant_by_schema_name(self, schema_name):
        """Cached tenant lookup by schema_name"""
        tenant_model = self.get_tenant_model()
        return tenant_model.objects.get(schema_name=schema_name)
    
    @lru_cache(maxsize=32)
    def _get_tenant_by_domain(self, domain):
        """Cached tenant lookup by domain"""
        domain_model = self.get_tenant_domain_model()
        domain_obj = domain_model.objects.get(domain=domain)
        return domain_obj.tenant
        
    def process_request(self, request):
        # Check for tenant header first
        tenant_from_header = request.headers.get('X-DTS-TENANT')
        
        if tenant_from_header:
            # Only log once per unique header value
            if tenant_from_header not in self._tenant_cache:
                logger.info(f"Tenant from header: {tenant_from_header}")
            
            try:
                # First check memory cache
                if tenant_from_header in self._tenant_cache:
                    tenant = self._tenant_cache[tenant_from_header]
                else:
                    # Then check function cache
                    tenant = self._get_tenant_by_schema_name(tenant_from_header)
                    # Update memory cache
                    self._tenant_cache[tenant_from_header] = tenant
                
                # Set tenant for this request
                connection.set_tenant(tenant)
                request.tenant = tenant
                
                # Only log once per unique header value
                if tenant_from_header not in self._tenant_cache:
                    logger.info(f"Successfully set tenant from header: {tenant.schema_name}")
                    # Add to cache to prevent duplicate logging
                    self._tenant_cache[tenant_from_header] = tenant
                return None
            except self.get_tenant_model().DoesNotExist:
                logger.error(f"Tenant from header not found: {tenant_from_header}")
                raise Http404(f"❌ Invalid tenant header: {tenant_from_header}")
            except Exception as e:
                logger.error(f"Error processing tenant header: {str(e)}")
                # Fall through to domain-based resolution
        
        # If no header or header processing failed, fallback to domain-based tenant
        # Limit this log to once per 10 requests by checking a counter
        if not hasattr(self, '_domain_log_counter'):
            self._domain_log_counter = 0
        self._domain_log_counter += 1
        if self._domain_log_counter >= 10:
            logger.info("Using domain-based tenant resolution")
            self._domain_log_counter = 0
            
        return super().process_request(request)
    
    def get_tenant(self, model, hostname):
        """Get tenant by hostname/domain"""
        try:
            # First check memory cache for the hostname
            if hostname in self._tenant_cache:
                return self._tenant_cache[hostname]
            
            # Extract subdomain from hostname
            hostname_parts = hostname.split('.')
            subdomain = hostname_parts[0] if len(hostname_parts) > 1 else None
            
            # Only log once per 10 requests for the same hostname
            if not hasattr(self, '_hostname_log_counter'):
                self._hostname_log_counter = {}
            if hostname not in self._hostname_log_counter:
                self._hostname_log_counter[hostname] = 0
            self._hostname_log_counter[hostname] += 1
            
            if self._hostname_log_counter[hostname] >= 10:
                logger.info(f"Getting tenant for hostname: {hostname}, subdomain: {subdomain}")
                self._hostname_log_counter[hostname] = 0
            
            # First try with function cache
            try:
                domain = self._get_tenant_by_domain(hostname)
                # Update memory cache
                self._tenant_cache[hostname] = domain
                return domain
            except self.get_tenant_domain_model().DoesNotExist:
                pass
                
            # If domain lookup fails, try by schema_name (assuming subdomain == schema_name)
            if subdomain and subdomain != 'localhost':
                # Don't log this every time
                if self._hostname_log_counter[hostname] == 1:
                    logger.info(f"Trying to get tenant by schema_name: {subdomain}")
                tenant = self._get_tenant_by_schema_name(subdomain)
                # Update memory cache
                self._tenant_cache[hostname] = tenant
                return tenant
            else:
                raise model.DoesNotExist("No valid subdomain")
        except model.DoesNotExist as e:
            # Only log errors occasionally to avoid log flooding
            if not hasattr(self, '_error_log_counter'):
                self._error_log_counter = 0
            self._error_log_counter += 1
            if self._error_log_counter >= 5:
                logger.error(f"Tenant error: {str(e)}")
                self._error_log_counter = 0
            raise Http404(f"❌ Invalid tenant. No tenant for hostname '{hostname}'")
    
    def activate_tenant(self, tenant, connection_obj=None):
        """Activate the tenant schema in the database connection"""
        # Use the provided connection or the default one
        from django.db import connection as default_connection
        conn = connection_obj or default_connection
        conn.set_tenant(tenant)
        # Only log this once per tenant to avoid log flooding
        if not hasattr(self, '_tenant_activation_log'):
            self._tenant_activation_log = set()
        
        tenant_id = tenant.schema_name
        if tenant_id not in self._tenant_activation_log:
            logger.info(f"Activated tenant: {tenant.schema_name}")
            self._tenant_activation_log.add(tenant_id)

