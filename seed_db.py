import os
import django
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_vehicle_share.settings')
django.setup()

from customers.models import User, Vehicle, Reservation, Payment, Report
from operators.models import MaintenanceRecord, ChargingRecord

def seed():
    print("Starting database seeding...")

    # 1. Create Users
    users_to_create = [
        {
            'username': 'manager1',
            'email': 'manager@example.com',
            'password': 'password123',
            'is_manager': True,
            'first_name': 'Main',
            'surname': 'Manager'
        },
        {
            'username': 'operator1',
            'email': 'operator@example.com',
            'password': 'password123',
            'is_operator': True,
            'first_name': 'Tech',
            'surname': 'Operator'
        },
        {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'password123',
            'is_customer': True,
            'first_name': 'John',
            'surname': 'Doe'
        },
        {
            'username': 'customer2',
            'email': 'customer2@example.com',
            'password': 'password123',
            'is_customer': True,
            'first_name': 'Jane',
            'surname': 'Smith'
        },
        {
            'username': 'goutham1',
            'email': 'goutham1@example.com',
            'password': 'password1',
            'is_customer': True,
            'first_name': 'Goutham',
            'surname': 'Customer'
        },
        {
            'username': 'goutham2',
            'email': 'goutham2@example.com',
            'password': 'password1',
            'is_operator': True,
            'first_name': 'Goutham',
            'surname': 'Operator'
        },
        {
            'username': 'goutham3',
            'email': 'goutham3@example.com',
            'password': 'password1',
            'is_manager': True,
            'first_name': 'Goutham',
            'surname': 'Manager'
        }
    ]

    for u_data in users_to_create:
        if not User.objects.filter(username=u_data['username']).exists():
            User.objects.create(
                username=u_data['username'],
                email=u_data['email'],
                password=make_password(u_data['password']),
                is_manager=u_data.get('is_manager', False),
                is_operator=u_data.get('is_operator', False),
                is_customer=u_data.get('is_customer', False),
                first_name=u_data['first_name'],
                surname=u_data['surname'],
                is_active=True
            )
            print(f"Created user: {u_data['username']}")

    # 2. Create Vehicles
    vehicles_data = [
        {
            'vehicle_name': 'Alpha Scooter',
            'vehicle_type': 'Scooter',
            'vehicle_model': 'X-100',
            'registration_number': 'ABC-123',
            'battery': 100,
            'is_available': True,
            'longitude': -4.2576,
            'latitude': 55.8642,
            'hourly_rate': 5.50
        },
        {
            'vehicle_name': 'Beta Scooter',
            'vehicle_type': 'Scooter',
            'vehicle_model': 'X-100',
            'registration_number': 'DEF-456',
            'battery': 15,
            'is_available': True,
            'longitude': -4.2433,
            'latitude': 55.8611,
            'hourly_rate': 5.00
        },
        {
            'vehicle_name': 'Gamma Bike',
            'vehicle_type': 'Bike',
            'vehicle_model': 'B-50',
            'registration_number': 'GHI-789',
            'battery': 80,
            'is_available': False,
            'is_defective': True,
            'longitude': -4.2611,
            'latitude': 55.8591,
            'hourly_rate': 7.50
        },
        {
            'vehicle_name': 'Delta Scooter',
            'vehicle_type': 'Scooter',
            'vehicle_model': 'X-200',
            'registration_number': 'JKL-012',
            'battery': 50,
            'is_available': True,
            'longitude': -4.2512,
            'latitude': 55.8711,
            'hourly_rate': 6.00
        },
        {
            'vehicle_name': 'Epsilon Scooter',
            'vehicle_type': 'Scooter',
            'vehicle_model': 'X-100',
            'registration_number': 'MNO-345',
            'battery': 0,
            'is_available': False,
            'longitude': -4.2655,
            'latitude': 55.8622,
            'hourly_rate': 4.50
        }
    ]

    for v_data in vehicles_data:
        if not Vehicle.objects.filter(registration_number=v_data['registration_number']).exists():
            Vehicle.objects.create(**v_data)
            print(f"Created vehicle: {v_data['registration_number']}")

    print("Seeding completed successfully.")

if __name__ == "__main__":
    seed()
