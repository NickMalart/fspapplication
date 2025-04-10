import os
import random
import django
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

# Import models after Django setup
from client.models import Client as ClientModel, ClientWarehouse
from faker import Faker
from tenant.models import Client as TenantClient
from django.db import connection

def create_fake_warehouses(tenant_schema='dev', client_name='Baldwin Group Services', count=100):
    """Create fake warehouses for a specific client in the given tenant"""
    # Connect to tenant
    try:
        tenant = TenantClient.objects.get(schema_name=tenant_schema)
        print(f"Found tenant: {tenant.name} (schema: {tenant.schema_name})")
    except TenantClient.DoesNotExist:
        print(f"Error: Tenant with schema '{tenant_schema}' not found")
        return
    
    # Set tenant connection
    connection.set_tenant(tenant)
    print(f"Connection set to tenant: {connection.tenant.schema_name}")
    
    # Find the client
    try:
        client = ClientModel.objects.get(name=client_name)
        print(f"Found client: {client.name} (ID: {client.id})")
    except ClientModel.DoesNotExist:
        print(f"Error: Client '{client_name}' not found in '{tenant_schema}' tenant")
        return
    
    fake = Faker('en_AU')  # Australian locale
    
    # Warehouse name prefixes/suffixes
    prefixes = ["Main", "North", "South", "East", "West", "Central", "Regional", 
                "Primary", "Secondary", "Auxiliary", "Distribution", "Storage",
                "Logistics", "Fulfillment", "National", "International", "Local"]
    
    suffixes = ["Warehouse", "Depot", "Hub", "Center", "Facility", "Distribution Center", 
                "Storage Facility", "Logistics Center", "Fulfillment Center"]
    
    # Australian states
    au_states = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']
    
    # Storage capacity descriptions
    storage_capacities = [
        "1,000 pallets / 500 sqm", 
        "2,500 pallets / 1,200 sqm", 
        "5,000 pallets / 2,500 sqm",
        "10,000 pallets / 4,500 sqm",
        "15,000 pallets / 7,000 sqm",
        "500 sqm with high-density racking",
        "1,500 sqm with automated storage",
        "3,000 sqm with drive-in racking",
        "8,000 sqm with selective racking",
        "20,000 sqm full service facility"
    ]
    
    # Operating hours templates
    operating_hours_templates = [
        "Mon-Fri: 9AM-5PM",
        "Mon-Fri: 8AM-6PM, Sat: 9AM-1PM",
        "24/7 Operation",
        "Mon-Fri: 7AM-7PM",
        "Mon-Sat: 6AM-10PM",
        "Mon-Fri: 6AM-6PM",
        "Mon-Thu: 7AM-8PM, Fri: 7AM-6PM",
        "Business hours: 8:30AM-5:30PM weekdays"
    ]
    
    # Special instructions
    special_instructions_templates = [
        "Forklift access required for all deliveries",
        "Call 30 minutes before arrival",
        "Security clearance needed for access",
        "Loading dock can accommodate vehicles up to 12 meters",
        "No deliveries accepted after 4PM",
        "Temperature-controlled environment - maintain 15-20°C",
        "Hazardous materials storage area requires special handling",
        "Please check in at main office before unloading",
        "Restricted access during public holidays",
        "Automated storage system - specific pallet dimensions required",
        "FIFO storage policy strictly enforced",
        "Driver's license ID required at security gate"
    ]
    
    # Popular first names
    first_names = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
        "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"
    ]
    
    # Popular last names
    last_names = [
        "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
        "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"
    ]
    
    print(f'Creating {count} fake warehouses for {client_name}...')
    
    warehouses_created = 0
    
    # Set first warehouse as primary
    is_primary = True
    
    for _ in range(count):
        # Generate warehouse name
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        
        # Sometimes use location in name
        if random.random() < 0.5:
            state = random.choice(au_states)
            warehouse_name = f"{prefix} {state} {suffix}"
        else:
            warehouse_name = f"{prefix} {suffix}"
        
        # Generate warehouse description
        descriptions = [
            f"Main {suffix.lower()} facility serving {random.choice(au_states)} region",
            f"Strategic {suffix.lower()} location for {random.choice(['regional', 'metropolitan', 'interstate', 'national'])} distribution",
            f"Specialized {suffix.lower()} with climate-controlled storage options",
            f"Full-service {suffix.lower()} with advanced inventory management systems",
            f"Modern {suffix.lower()} with integrated logistics capabilities"
        ]
        description = random.choice(descriptions)
        
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
        
        # Generate contact details
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        contact_email = f"{first_name.lower()}.{last_name.lower()}@{client_name.lower().replace(' ', '')}.com.au"
        
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
        ]
        contact_phone = fake.numerify(random.choice(phone_formats))
        
        # Warehouse operational details
        operating_hours = random.choice(operating_hours_templates)
        storage_capacity = random.choice(storage_capacities)
        
        # 60% chance to have special instructions
        if random.random() < 0.6:
            special_instructions = random.choice(special_instructions_templates)
        else:
            special_instructions = ""
            
        # Create warehouse object
        try:
            warehouse = ClientWarehouse.objects.create(
                id=uuid.uuid4(),
                client=client,
                name=warehouse_name,
                description=description,
                street_number=street_number,
                street_name=street_name,
                suburb=suburb,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                latitude=latitude,
                longitude=longitude,
                first_name=first_name,
                last_name=last_name,
                contact_phone=contact_phone,
                contact_email=contact_email,
                is_primary=is_primary,
                operating_hours=operating_hours,
                storage_capacity=storage_capacity,
                special_instructions=special_instructions,
                is_active=True
            )
            warehouses_created += 1
            
            # After first warehouse, the rest are secondary
            if is_primary:
                is_primary = False
                
            print(f"Created warehouse: {warehouse_name} (ID: {warehouse.id})")
        except Exception as e:
            print(f"Error creating warehouse {warehouse_name}: {e}")
    
    print(f'Successfully created {warehouses_created} fake warehouses for {client_name}')

if __name__ == '__main__':
    create_fake_warehouses('dev', 'Adams Group', 100) 