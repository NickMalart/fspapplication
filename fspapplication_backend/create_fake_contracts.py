import os
import random
import django
import uuid
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

# Now import Django models
from client.models import Client as ClientModel, ClientContract
from faker import Faker
from tenant.models import Client as TenantClient
from django.db import connection

def create_fake_contracts_for_client(tenant_schema='dev', client_id='ffe3cedc-71bd-440b-b6cb-44281bc8d49a', num_contracts=100):
    """Create fake contracts for a specific client in a tenant"""
    # Get the tenant by schema name
    try:
        tenant = TenantClient.objects.get(schema_name=tenant_schema)
        print(f"Found tenant: {tenant.name} (schema: {tenant.schema_name})")
    except TenantClient.DoesNotExist:
        print(f"Error: Tenant with schema '{tenant_schema}' not found")
        return
    
    # Set tenant connection
    connection.set_tenant(tenant)
    print(f"Connection set to tenant: {connection.tenant.schema_name}")
    
    fake = Faker()
    
    # Get the specific client by UUID
    try:
        client = ClientModel.objects.get(id=client_id)
        print(f'Found client: {client.name} (ID: {client.id})')
    except ClientModel.DoesNotExist:
        print(f"Error: Client with ID '{client_id}' not found")
        return

    # Contract types and suffixes to make names more realistic
    contract_types = [
        'Service Agreement',
        'Maintenance Contract',
        'Support Agreement',
        'License Agreement',
        'Subscription',
        'Partnership Agreement',
        'Consulting Agreement',
        'Development Contract',
        'Managed Services',
        'Professional Services',
        'Training Agreement',
        'Implementation Contract',
        'Software License',
        'Hardware Support',
        'Cloud Services',
        'Security Services',
        'Data Management',
        'Network Services',
        'Infrastructure Support',
        'Technical Support'
    ]
    
    contract_suffixes = [
        'Standard',
        'Premium',
        'Enterprise',
        'Basic',
        'Pro',
        'Custom',
        'Extended',
        'Limited',
        'Plus',
        'Advanced',
        'Essential',
        'Professional',
        'Corporate',
        'Business',
        'Elite'
    ]

    contracts_created = 0
    
    for i in range(num_contracts):
        # Generate contract name
        contract_type = random.choice(contract_types)
        if random.random() < 0.7:  # 70% chance to add a suffix
            contract_name = f"{client.name} - {contract_type} ({random.choice(contract_suffixes)}) #{i+1}"
        else:
            contract_name = f"{client.name} - {contract_type} #{i+1}"

        # Generate description
        descriptions = [
            f"Standard {contract_type.lower()} for {client.name}'s business operations.",
            f"Customized {contract_type.lower()} tailored to {client.name}'s specific needs.",
            f"Comprehensive {contract_type.lower()} covering all aspects of service delivery.",
            f"Specialized {contract_type.lower()} focusing on key business requirements.",
            f"Extended {contract_type.lower()} with additional support and maintenance terms.",
            f"Premium {contract_type.lower()} package with enhanced features and support.",
            f"Enterprise-level {contract_type.lower()} solution for {client.name}.",
            f"Advanced {contract_type.lower()} with 24/7 support and monitoring.",
            f"Professional {contract_type.lower()} with dedicated account management.",
            f"Custom {contract_type.lower()} designed for {client.name}'s industry needs."
        ]
        description = random.choice(descriptions)

        # Randomly decide if contract is active (85% active, 15% inactive)
        is_active = random.random() < 0.85

        try:
            contract = ClientContract.objects.create(
                id=uuid.uuid4(),
                client=client,
                name=contract_name,
                description=description,
                is_active=is_active
            )
            contracts_created += 1
            print(f"Created contract {contracts_created}/{num_contracts}: {contract_name}")
        except Exception as e:
            print(f"Error creating contract for client {client.name}: {e}")

    print(f'Successfully created {contracts_created} fake contracts for client {client.name}')

if __name__ == '__main__':
    create_fake_contracts_for_client('dev', 'ffe3cedc-71bd-440b-b6cb-44281bc8d49a', 100) 