from django.db import connection
from django.utils import timezone
import logging

from .models import Client, SubscriptionPlan

logger = logging.getLogger(__name__)

class SubscriptionService:
    """Service for managing tenant subscriptions and user billing"""
    
    @staticmethod
    def update_tenant_subscription(tenant_id, plan_id, billing_frequency='monthly'):
        """
        Update a tenant's subscription plan
        
        Args:
            tenant_id: The ID of the tenant/client to update
            plan_id: The ID of the subscription plan to assign
            billing_frequency: 'monthly' or 'yearly'
        
        Returns:
            tuple: (success, message)
        """
        try:
            client = Client.objects.get(id=tenant_id)
            plan = SubscriptionPlan.objects.get(id=plan_id)
            
            # Update subscription details
            client.subscription_plan = plan
            client.billing_frequency = billing_frequency
            client.subscription_start_date = timezone.now().date()
            # For yearly billing, set end date to 1 year from now
            if billing_frequency == 'yearly':
                client.subscription_end_date = timezone.now().date().replace(year=timezone.now().date().year + 1)
            else:
                # For monthly, set end date to 1 month from now
                today = timezone.now().date()
                next_month = today.month + 1
                next_year = today.year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                client.subscription_end_date = today.replace(month=next_month, year=next_year)
            
            client.is_subscription_active = True
            client.save()
            
            return True, f"Successfully updated subscription to {plan.name}"
        except Client.DoesNotExist:
            return False, "Tenant not found"
        except SubscriptionPlan.DoesNotExist:
            return False, "Subscription plan not found"
        except Exception as e:
            logger.error(f"Error updating subscription: {str(e)}")
            return False, f"Error updating subscription: {str(e)}"
    
    @staticmethod
    def update_paid_user_count(tenant_id, new_paid_count):
        """
        Update the number of paid users for a tenant
        
        Args:
            tenant_id: The ID of the tenant/client
            new_paid_count: The new number of paid users
        
        Returns:
            tuple: (success, message)
        """
        try:
            client = Client.objects.get(id=tenant_id)
            client.paid_user_count = new_paid_count
            client.save()
            return True, f"Successfully updated paid user count to {new_paid_count}"
        except Client.DoesNotExist:
            return False, "Tenant not found"
        except Exception as e:
            logger.error(f"Error updating paid user count: {str(e)}")
            return False, f"Error updating paid user count: {str(e)}"
    
    @staticmethod
    def check_tenant_billing_status(tenant_id):
        """
        Check if a tenant needs to update their billing
        
        Args:
            tenant_id: The ID of the tenant/client
            
        Returns:
            dict: Information about the tenant's billing status
        """
        try:
            client = Client.objects.get(id=tenant_id)
            current_user_count = client.get_current_user_count()
            
            return {
                'current_user_count': current_user_count,
                'paid_user_count': client.paid_user_count,
                'needs_payment_update': client.needs_payment_update(),
                'current_plan': client.subscription_plan.name if client.subscription_plan else None,
                'billing_frequency': client.billing_frequency,
                'is_active': client.is_subscription_active,
                'monthly_cost': client.calculate_monthly_cost() if client.subscription_plan else 0,
            }
        except Client.DoesNotExist:
            return {'error': 'Tenant not found'}
        except Exception as e:
            logger.error(f"Error checking billing status: {str(e)}")
            return {'error': f"Error checking billing status: {str(e)}"} 