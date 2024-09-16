import json
import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task
from users.models import User, Customer


class WorkerTaskAPITestCase(APITestCase):
    clean_password = None
    user=None
    fixtures = ['test_users_backup.json', 'test_customer_backup.json',
                'test_worker_backup.json', 'test_tasks_backup.json']

    @classmethod
    def setUpTestData(cls):
        customer = Customer.objects.last()
        cls.task_1 = Task.objects.create(title='Test task 1', customer=customer)
        cls.task_2 = Task.objects.create(title='Test task 2', customer=customer)
        cls.task_3 = Task.objects.create(title='Test task 3', customer=customer)
        cls.setUpTestUser()
        worker = cls.user.worker
        cls.task_4 = Task.objects.create(title='Test task 4', customer=customer, worker=worker)

    @classmethod
    def setUpTestUser(cls):
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='Test_1',
                                            phone='+375291850665',
                                            type='worker'
                                            )

    def setUp(self):
        self.jwt_auth(user=self.user)

    def jwt_auth(self, user):
        url = reverse('token_obtain_pair')
        auth = self.client.post(url,
                                {'username': user.username, 'password': self.clean_password},
                                format='json')

        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))

    def test_api_jwt(self):
        url = reverse('token_obtain_pair')
        auth = self.client.post(url,
                                {'username': self.user.username,
                                 'password': self.clean_password},
                                format='json')

        self.assertEqual(auth.status_code, status.HTTP_200_OK)

    def test_get_list(self):
        url = reverse('tasks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_id = self.user.id
        task_list = response.data
        for task in task_list:
            with self.subTest(task=task):
                worker = task['worker']
                self.assertIn(worker, [user_id, None])

    def test_get_detail(self):
        url = reverse('tasks-detail', args=(self.task_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @unittest.expectedFailure
    def test_get_detail_fail(self):
        url = reverse('tasks-detail', args=(61,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_take_in_process(self):
        url = reverse('tasks-detail', args=(self.task_1.id,))
        data = {'status': 'in_process'}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.task_1.refresh_from_db()
        self.assertEqual(self.user.worker, self.task_1.worker)
        self.assertEqual('in_process', self.task_1.status)

    @unittest.expectedFailure
    def test_patch_take_in_process_fail(self):
        url = reverse('tasks-detail', args=(61,))
        data = {'status': 'in_process'}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.task_1.refresh_from_db()
        self.assertEqual(self.user.worker, self.task_1.worker)
        self.assertEqual('in_process', self.task_1.status)

