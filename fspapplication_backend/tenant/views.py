from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import SubscriptionPlan, Client
from .services import SubscriptionService
from .serializers import SubscriptionPlanSerializer, ClientSerializer

class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view available subscription plans.
    """
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated]

class TenantSubscriptionViewSet(viewsets.GenericViewSet):
    """
    API endpoint to manage tenant subscriptions.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def current_subscription(self, request):
        """Get current tenant's subscription details"""
        from django.db import connection
        
        try:
            tenant = Client.objects.get(schema_name=connection.schema_name)
            billing_status = SubscriptionService.check_tenant_billing_status(tenant.id)
            return Response(billing_status)
        except Client.DoesNotExist:
            return Response(
                {"error": "Tenant not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def update_subscription(self, request):
        """Update the tenant's subscription plan"""
        from django.db import connection
        
        plan_id = request.data.get('plan_id')
        billing_frequency = request.data.get('billing_frequency', 'monthly')
        
        if not plan_id:
            return Response(
                {"error": "plan_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            tenant = Client.objects.get(schema_name=connection.schema_name)
            success, message = SubscriptionService.update_tenant_subscription(
                tenant.id, plan_id, billing_frequency
            )
            
            if success:
                return Response({"message": message})
            else:
                return Response(
                    {"error": message}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Client.DoesNotExist:
            return Response(
                {"error": "Tenant not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def update_user_count(self, request):
        """Update the tenant's paid user count"""
        from django.db import connection
        
        new_count = request.data.get('paid_user_count')
        
        if new_count is None:
            return Response(
                {"error": "paid_user_count is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_count = int(new_count)
        except ValueError:
            return Response(
                {"error": "paid_user_count must be an integer"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            tenant = Client.objects.get(schema_name=connection.schema_name)
            current_count = tenant.get_current_user_count()
            
            if new_count < current_count:
                return Response(
                    {"error": f"Cannot set paid user count ({new_count}) lower than current user count ({current_count})"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            success, message = SubscriptionService.update_paid_user_count(
                tenant.id, new_count
            )
            
            if success:
                return Response({"message": message})
            else:
                return Response(
                    {"error": message}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Client.DoesNotExist:
            return Response(
                {"error": "Tenant not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
