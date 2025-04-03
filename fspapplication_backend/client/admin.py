from django.contrib import admin
from .models import Client, ClientWarehouse, ClientContract

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'abn', 'email', 'phone', 'is_active')
    search_fields = ('name', 'abn', 'email')
    list_filter = ('is_active', 'created_at')

@admin.register(ClientWarehouse)
class ClientWarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'city', 'is_primary', 'is_active')
    search_fields = ('name', 'client__name')
    list_filter = ('is_active', 'is_primary')

@admin.register(ClientContract)
class ClientContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'client')
    search_fields = ('name', 'client__name')
    list_filter = ('client',)
