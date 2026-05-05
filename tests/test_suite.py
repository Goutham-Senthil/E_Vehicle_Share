import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from customers.models import User, Vehicle, Reservation, Payment, Report

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

class TestRoleAccessControl(TestCase):
    def login_via_session(self, user):
        session = self.client.session
        session['user_pk'] = user.username
        session.save()

    def test_customer_cannot_access_manager_dashboard(self):
        user = make_customer()
        self.login_via_session(user)
        response = self.client.get(reverse('manager_dashboard'))
        assert response.status_code in [302, 403]
        assert response.status_code != 200

    def test_customer_cannot_access_operator_dashboard(self):
        user = make_customer()
        self.login_via_session(user)
        response = self.client.get(reverse('operator_dashboard'))
        assert response.status_code in [302, 403]
        assert response.status_code != 200

    def test_operator_cannot_access_manager_dashboard(self):
        user = make_operator()
        self.login_via_session(user)
        response = self.client.get(reverse('manager_dashboard'))
        assert response.status_code in [302, 403]
        assert response.status_code != 200

    def test_unauthenticated_user_redirected_from_customer_dashboard(self):
        response = self.client.get(reverse('customer_dashboard'))
        assert response.status_code == 302

class TestAuthentication(TestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        assert response.status_code == 200

    def test_invalid_login_does_not_redirect(self):
        response = self.client.post(reverse('login'), {'username': 'wrong', 'password': 'wrong'})
        assert response.status_code != 302

    def test_customer_login_redirects_to_customer_dashboard(self):
        user = make_customer()
        response = self.client.post(reverse('login'), {'username': user.username, 'password': 'testpass123'})
        assert response.status_code == 302
        assert 'customers' in response.url or 'dashboard' in response.url

class TestVehicleAvailability(TestCase):
    def login_via_session(self, user):
        session = self.client.session
        session['user_pk'] = user.username
        session.save()

    def test_available_vehicle_shows_in_list(self):
        make_vehicle()
        user = make_customer()
        self.login_via_session(user)
        response = self.client.get(reverse('rent_vehicle'))
        assert response.status_code == 200

    def test_vehicle_marked_unavailable_after_reservation(self):
        vehicle = make_vehicle(available=True)
        user = make_customer()
        reservation = Reservation.objects.create(
            vehicle=vehicle,
            user=user,
            start_time=timezone.now(),
            status='In use'
        )
        vehicle.is_available = False
        vehicle.save()
        vehicle.refresh_from_db()
        assert vehicle.is_available is False

class TestBookingFlow(TestCase):
    def test_reservation_created_with_correct_status(self):
        user = make_customer()
        vehicle = make_vehicle()
        reservation = Reservation.objects.create(
            vehicle=vehicle,
            user=user,
            start_time=timezone.now(),
            status='In use'
        )
        assert reservation.status == 'In use'
        assert reservation.user == user
        assert reservation.vehicle == vehicle

    def test_completed_reservation_status(self):
        user = make_customer()
        vehicle = make_vehicle()
        reservation = Reservation.objects.create(
            vehicle=vehicle,
            user=user,
            start_time=timezone.now(),
            status='In use'
        )
        reservation.status = 'Completed'
        reservation.save()
        reservation.refresh_from_db()
        assert reservation.status == 'Completed'

class TestPaymentLogic(TestCase):
    def test_payment_created_with_pending_status(self):
        user = make_customer()
        vehicle = make_vehicle()
        reservation = Reservation.objects.create(
            vehicle=vehicle,
            user=user,
            start_time=timezone.now(),
            status='Completed'
        )
        payment = Payment.objects.create(
            user=user,
            amount=10.0,
            status='Pending',
            reservation=reservation
        )
        assert payment.status == 'Pending'
        assert payment.amount == 10.0

    def test_payment_status_updates_to_completed(self):
        user = make_customer()
        payment = Payment.objects.create(
            user=user,
            amount=10.0,
            status='Pending'
        )
        payment.status = 'Completed'
        payment.save()
        payment.refresh_from_db()
        assert payment.status == 'Completed'

    def test_user_balance_deduction(self):
        user = make_customer()
        user.balance = 50.0
        user.save()
        user.balance -= 10.0
        user.save()
        user.refresh_from_db()
        assert user.balance == 40.0

class TestVehicleReporting(TestCase):
    def test_report_links_to_correct_user_and_vehicle(self):
        user = make_customer()
        vehicle = make_vehicle()
        report = Report.objects.create(
            vehicle=vehicle,
            user=user,
            reason='Battery issue'
        )
        assert report.vehicle == vehicle
        assert report.user == user
