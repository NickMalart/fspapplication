from django.http import HttpResponseForbidden
from django.urls import resolve
from django.db import connection
from tenant.models import Client

class TenantUserLimitMiddleware:
    """
    Middleware to enforce tenant user limits based on their subscription plan.
    This middleware checks user creation endpoints and blocks them if the tenant has reached its user limit.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip middleware if we're not in a tenant schema
        if connection.schema_name == 'public':
            return None
            
        # Check if this is a user creation endpoint
        resolved = resolve(request.path_info)
        
        # List of URL patterns that create users
        user_creation_patterns = [
            'user-list', 'register', 'create-user', 'add-user'
        ]
        
        if (resolved.url_name in user_creation_patterns and 
            request.method in ['POST']):
            
            # Get current tenant
            try:
                tenant = Client.objects.get(schema_name=connection.schema_name)
                current_count = tenant.get_current_user_count()
                
                # Check if subscription is active
                if not tenant.is_subscription_active:
                    return HttpResponseForbidden(
                        "Your subscription is inactive. "
                        "Please update your subscription to add users."
                    )
                
                # Check if tenant needs to update their payment
                if tenant.needs_payment_update():
                    return HttpResponseForbidden(
                        f"You currently have {current_count} users, but have only paid for {tenant.paid_user_count}. "
                        "Please update your subscription billing before adding more users."
                    )
                    
            except Client.DoesNotExist:
                # This shouldn't happen, but just in case
                pass
                
        return None 