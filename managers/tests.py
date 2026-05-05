from django.test import TestCase
from django.urls import reverse
from tests.test_helpers import make_manager, login_via_session

class TestManagerWorkflows(TestCase):
    def test_manager_can_access_dashboard(self):
        user = make_manager()
        login_via_session(self.client, user)
        response = self.client.get(reverse('manager_dashboard'))
        assert response.status_code == 200
