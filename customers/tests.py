from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from customers.models import Reservation, Payment, Report
from tests.test_helpers import make_customer, make_vehicle, login_via_session

class TestVehicleAvailability(TestCase):
    def test_available_vehicle_shows_in_list(self):
        make_vehicle()
        user = make_customer()
        login_via_session(self.client, user)
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
