import pytest
from customers.models import User, Vehicle
from django.utils import timezone

def login_via_session(client, user):
    """
    Helper to bypass custom middleware authentication by setting the session user_pk.
    """
    session = client.session
    session['user_pk'] = user.pk
    session.save()

def make_customer(username='testcustomer', password='testpass123'):
    user = User.objects.create(username=username, is_customer=True, is_active=True)
    user.set_password(password)
    user.save()
    return user

def make_operator(username='testoperator', password='testpass123'):
    user = User.objects.create(username=username, is_operator=True, is_active=True)
    user.set_password(password)
    user.save()
    return user

def make_manager(username='testmanager', password='testpass123'):
    user = User.objects.create(username=username, is_manager=True, is_active=True)
    user.set_password(password)
    user.save()
    return user

def make_vehicle(registration='REG001', available=True, battery=80, rate=5.0):
    return Vehicle.objects.create(
        vehicle_type='Scooter',
        vehicle_name='Test Scooter',
        vehicle_model='Model X',
        registration_number=registration,
        battery=battery,
        is_available=available,
        longitude=0.0,
        latitude=0.0,
        hourly_rate=rate
    )
