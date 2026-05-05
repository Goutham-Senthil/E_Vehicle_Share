from django.test import TestCase
from django.urls import reverse
from tests.test_helpers import make_operator, make_vehicle, login_via_session

class TestOperatorWorkflows(TestCase):
    def test_charge_vehicle_updates_battery_and_availability(self):
        # Create an empty battery vehicle that is unavailable
        vehicle = make_vehicle(battery=0, available=False)
        user = make_operator()
        login_via_session(self.client, user)
        
        # Call the charge endpoint
        response = self.client.post(reverse('charge_vehicle', args=[vehicle.vehicle_id]))
        assert response.status_code == 302
        
        vehicle.refresh_from_db()
        assert vehicle.battery == 100
        assert vehicle.is_available is True

    def test_repair_vehicle_updates_defective_status(self):
        # Create a defective vehicle
        vehicle = make_vehicle()
        vehicle.is_defective = True
        vehicle.is_available = False
        vehicle.save()
        
        user = make_operator()
        login_via_session(self.client, user)
        
        # Call the repair endpoint
        response = self.client.post(reverse('repair_vehicle', args=[vehicle.vehicle_id]))
        assert response.status_code == 302
        
        vehicle.refresh_from_db()
        assert vehicle.is_defective is False
        # Note: Availability might depend on battery, but the repair should at least clear defective
