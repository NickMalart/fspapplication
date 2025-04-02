import os
import random
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

# Now import Django models (only after setting up the environment)
from client.models import Client as ClientModel
from faker import Faker
from tenant.models import Client as TenantClient
from django.db import connection

def create_fake_clients(tenant_schema='dev', count=100):
    """Create fake clients with random data for a specific tenant"""
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
    
    fake = Faker('en_AU')  # Australian locale for proper ABN and phone formats
    
    # List of company types to make names more realistic
    company_types = ['Pty Ltd', 'Ltd', 'Inc', 'Limited', 'Holdings', 'Group', 'Partners', 'Industries', 'Services']
    
    # List of domain extensions
    domain_extensions = ['com.au', 'com', 'net.au', 'net', 'org', 'co', 'io', 'tech', 'digital']
    
    print(f'Creating {count} fake clients for tenant {tenant.name}...')
    
    clients_created = 0
    
    for _ in range(count):
        # Generate company name
        company_name = fake.company()
        if random.random() < 0.7:  # 70% chance to add a company type
            company_name = f"{company_name} {random.choice(company_types)}"
            
        # Remove any Ltd/Pty Ltd that might be in the original name to avoid duplication
        company_name = company_name.replace(' Ltd', '').replace(' Pty', '')
        
        # Generate ABN (11 digits Australian Business Number)
        abn = ' '.join([fake.numerify('##') for _ in range(5)]).strip()
        
        # Generate company domain based on name
        company_slug = company_name.lower().replace(',', '').replace('.', '')
        company_slug = ''.join(c for c in company_slug if c.isalnum() or c.isspace()).replace(' ', '')
        domain_extension = random.choice(domain_extensions)
        domain = f"{company_slug}.{domain_extension}"
        
        # Generate email and website
        email = f"info@{domain}"
        website = f"https://www.{domain}"
        
        # Generate phone (Australian format)
        phone_formats = [
            '+61 2 #### ####',  # Sydney/NSW
            '+61 3 #### ####',  # Melbourne/VIC
            '+61 7 #### ####',  # Brisbane/QLD
            '+61 8 #### ####',  # Perth/WA, Adelaide/SA
            '02 #### ####',     # NSW local format
            '03 #### ####',     # VIC local format
            '07 #### ####',     # QLD local format
            '08 #### ####',     # WA/SA local format
            '1300 ### ###',     # Business numbers
            '1800 ### ###'      # Toll free
        ]
        phone = fake.numerify(random.choice(phone_formats))
        
        # Randomly decide if client is active (80% active, 20% inactive)
        is_active = random.random() < 0.8
        
        # Create client object
        try:
            client = ClientModel.objects.create(
                name=company_name,
                abn=abn,
                email=email,
                phone=phone,
                website=website,
                is_active=is_active
            )
            clients_created += 1
            print(f"Created client: {company_name} (ABN: {abn})")
        except Exception as e:
            print(f"Error creating client {company_name}: {e}")
    
    print(f'Successfully created {clients_created} fake clients for tenant {tenant.name}')

if __name__ == '__main__':
    create_fake_clients('dev', 100) 