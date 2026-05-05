from django.test import TestCase
from django.urls import reverse
from tests.test_helpers import make_customer, make_operator, make_manager, login_via_session

class TestRoleAccessControl(TestCase):
    def test_customer_cannot_access_manager_dashboard(self):
        user = make_customer()
        login_via_session(self.client, user)
        response = self.client.get(reverse('manager_dashboard'))
        assert response.status_code in [302, 403]
        assert response.status_code != 200

    def test_customer_cannot_access_operator_dashboard(self):
        user = make_customer()
        login_via_session(self.client, user)
        response = self.client.get(reverse('operator_dashboard'))
        assert response.status_code in [302, 403]
        assert response.status_code != 200

    def test_operator_cannot_access_manager_dashboard(self):
        user = make_operator()
        login_via_session(self.client, user)
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
