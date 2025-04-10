import os
import random
import django
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

# Now import Django models
from agent.models import Agent
from faker import Faker
from tenant.models import Client as TenantClient
from django.db import connection

def create_fake_agents(tenant_schema='dev', count=100):
    """Create fake agents with random data for a specific tenant"""
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
    company_types = ['Logistics', 'Transport', 'Freight', 'Shipping', 'Carriers', 'Haulage', 'Delivery', 
                     'Express', 'Courier', 'Distribution', 'Agents', 'Services', 'Partners', 'Associates']
    
    # List of domain extensions
    domain_extensions = ['com.au', 'com', 'net.au', 'net', 'org', 'co', 'io', 'logistics', 'transport']
    
    # Australian states
    au_states = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']
    
    print(f'Creating {count} fake agents for tenant {tenant.name}...')
    
    agents_created = 0
    
    for _ in range(count):
        # Generate agent name
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
        
        # Generate S3 path for logo (no actual file, just a placeholder path)
        logo = f"s3://agent-logos/{company_slug}-logo.png" if random.random() < 0.8 else None
        
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
        
        # Generate address data
        street_number = fake.building_number()
        street_name = fake.street_name()
        suburb = fake.city()
        city = suburb  # In Australia, suburb and city can be the same
        state = random.choice(au_states)
        postal_code = fake.postcode()
        country = 'Australia'
        
        # Generate random coordinates within Australia
        latitude = random.uniform(-39.0, -33.0)  # Approximate latitude range for main Australian cities
        longitude = random.uniform(140.0, 153.0)  # Approximate longitude range for main Australian cities
        
        # Format coordinates to ensure they're within database limits
        latitude = round(latitude, 6)  # 6 decimal places for latitude
        longitude = round(longitude, 9)  # 9 decimal places for longitude
        
        # Randomly decide if agent is active (85% active, 15% inactive)
        is_active = random.random() < 0.85
        
        # Create agent object
        try:
            agent = Agent.objects.create(
                id=uuid.uuid4(),
                name=company_name,
                logo=logo,
                abn=abn,
                website=website,
                email=email,
                phone=phone,
                street_number=street_number,
                street_name=street_name,
                suburb=suburb,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                latitude=latitude,
                longitude=longitude,
                is_active=is_active
            )
            agents_created += 1
            print(f"Created agent: {company_name} (ID: {agent.id}, ABN: {abn})")
        except Exception as e:
            print(f"Error creating agent {company_name}: {e}")
    
    print(f'Successfully created {agents_created} fake agents for tenant {tenant.name}')

if __name__ == '__main__':
    create_fake_agents('dev', 100) 