import json

from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase

from tasks.models import Task
from users.models import User


class AnonymousTaskAPITestCase(APITestCase):
    """Тестирование запросов работника"""

    @classmethod
    def setUpTestData(cls):
        print('\nAnonimus tasks test:')
        cls.user_customer = User.objects.create(password='customer_super_ps_387', username='anon_api_test_customer_1')

        customer = cls.user_customer.customer
        cls.task = Task.objects.create(title='Customer test task_1 (wait)', customer=customer)

    def test_api_jwt(self):
        url = reverse('token_obtain_pair')
        auth_response = self.client.post(url,
                                         {'username': 'vasia',
                                          'password': 'random'},
                                         format='json')

        self.assertEqual(auth_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list(self):
        url = reverse('tasks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post(self):
        url = reverse('tasks-list')
        data = {
            "title": "test_task"
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        data = {'title': 'new_title'}
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_take_wait_task_in_process(self):
        url = reverse('tasks-take-in-process', args=(self.task.id,))
        response = self.client.patch(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
