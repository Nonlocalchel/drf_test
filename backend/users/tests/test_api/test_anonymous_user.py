from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase


class AnonymousAPITestCase(APITestCase):
    """Testing user data requests for unauthorized users"""

    @classmethod
    def setUpTestData(cls):
        print('\nAnonimus user test:')

    def test_api_jwt(self):
        """Authorized with user jwt"""
        url = reverse('token_obtain_pair')
        auth_response = self.client.post(url,
                                         {'username': 'vasia',
                                          'password': 'random'},
                                         format='json')

        self.assertEqual(auth_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list(self):
        """Get users list"""
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user(self):
        """Create user"""
        url = reverse('users-list')
        data = {
            "username": "test_user_hz",
            'password': 'super_ps'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
