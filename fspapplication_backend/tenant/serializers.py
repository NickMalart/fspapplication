from rest_framework import serializers
from .models import SubscriptionPlan, Client, Domain

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer for SubscriptionPlan model"""
    
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'plan_type', 'description', 
            'base_price_monthly', 'base_price_yearly',
            'price_per_user_monthly', 'price_per_user_yearly',
            'included_users', 'features', 'is_active'
        ]

class DomainSerializer(serializers.ModelSerializer):
    """Serializer for Domain model"""
    
    class Meta:
        model = Domain
        fields = ['id', 'domain', 'is_primary', 'tenant']

class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client (tenant) model"""
    domains = DomainSerializer(many=True, read_only=True)
    current_user_count = serializers.SerializerMethodField()
    subscription_plan_details = SubscriptionPlanSerializer(source='subscription_plan', read_only=True)
    monthly_cost = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'schema_name', 'created_on',
            'subscription_plan', 'subscription_plan_details',
            'subscription_start_date', 'subscription_end_date',
            'is_subscription_active', 'billing_frequency',
            'paid_user_count', 'current_user_count',
            'monthly_cost', 'domains'
        ]
        read_only_fields = [
            'id', 'schema_name', 'created_on', 
            'current_user_count', 'monthly_cost'
        ]
    
    def get_current_user_count(self, obj):
        """Get the current number of users for this tenant"""
        return obj.get_current_user_count()
    
    def get_monthly_cost(self, obj):
        """Get the monthly cost for this tenant"""
        return obj.calculate_monthly_cost() 