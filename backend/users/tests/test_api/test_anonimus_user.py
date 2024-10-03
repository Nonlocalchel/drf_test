import json

from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase

from tasks.models import Task


class AnonimusAPITestCase(APITestCase):
    """Тестирование запросов работника"""

    fixtures = [
        'users/tests/fixtures/only_users_backup.json',
        'users/tests/fixtures/customers_data_backup.json', 'users/tests/fixtures/workers_data_backup.json',
        'tasks/tests/fixtures/task_test_backup.json'
    ]

    @classmethod
    def setUpTestData(cls):
        print('\nAnonimus user test:')

    def test_api_jwt(self):
        url = reverse('token_obtain_pair')
        auth_response = self.client.post(url,
                                         {'username': 'vasia',
                                          'password': 'random'},
                                         format='json')

        self.assertEqual(auth_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list(self):
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user(self):
        url = reverse('users-list')
        data = {
            "username": "test_user_hz",
            'password': 'super_ps'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
