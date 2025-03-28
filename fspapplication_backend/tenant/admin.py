from django.contrib import admin
from .models import SubscriptionPlan, Client, Domain

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'base_price_monthly', 'price_per_user_monthly', 'included_users', 'is_active')
    list_filter = ('plan_type', 'is_active')
    search_fields = ('name', 'description')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'subscription_plan', 'is_subscription_active', 
                    'paid_user_count', 'get_current_users', 'get_monthly_cost')
    list_filter = ('is_subscription_active', 'subscription_plan')
    search_fields = ('name', 'schema_name')
    readonly_fields = ('get_current_users', 'get_monthly_cost')
    
    def get_current_users(self, obj):
        return obj.get_current_user_count()
    get_current_users.short_description = 'Current Users'
    
    def get_monthly_cost(self, obj):
        return f"${obj.calculate_monthly_cost()}"
    get_monthly_cost.short_description = 'Monthly Cost'

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('domain', 'tenant__name')
