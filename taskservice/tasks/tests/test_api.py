from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task
from users.models import User


class WorkerTaskAPITestCase(APITestCase):
    def setUp(self):
        self.test_user_data = {
            'password': 'worker_super_ps_387',
            'username': 'Test_1',
            'phone': '+37529542173',
            'type': 'worker'
        }
        self.test_user = User.objects.create_user(password=self.test_user_data['password'],
                                             username=self.test_user_data['username'],
                                             phone=self.test_user_data['phone'], type=self.test_user_data['type']
                                             )
        user = User.objects.create_user(password='customer_super_ps_387',
                                            username='customer_1',
                                            phone='+3752981343', type='customer'
                                            )
        self.task_1 = Task.objects.create(title='Test task 1', customer=user.customer)
        self.task_2 = Task.objects.create(title='Test task 2', customer=user.customer)
        self.task_3 = Task.objects.create(title='Test task 3', customer=user.customer)

    def test_api_jwt(self):
        url = reverse('token_obtain_pair')
        auth = self.client.post(url,
                                {'username': self.test_user_data['username'],
                                 'password': self.test_user_data['password']},
                                format='json')

        self.assertEqual(auth.status_code, status.HTTP_200_OK)

    def test_get_list(self):
        self.jwt_auth(user=self.test_user)

        url = reverse('tasks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def jwt_auth(self, user):
        url = reverse('token_obtain_pair')
        auth = self.client.post(url,
                                {'username': user.username, 'password': self.test_user_data['password']},
                                format='json')

        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))


