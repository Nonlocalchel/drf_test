import json

from django.db.models import Q
from django.urls import reverse
from rest_framework import status

from services.ImageWorker import ImageCreator
from tasks.models import Task
from services.APITestCaseWithJWT import APITestCaseWithJWT
from users.models import User, Worker, Customer


class CustomerTaskAPITestCase(APITestCaseWithJWT):
    """Тестирование запросов заказчика"""
    image_creator = ImageCreator

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('\nCustomer tasks test:')
        cls.user_customer = User.objects.create(password='customer_super_ps_387', username='cu_api_test_customer_1')
        cls.user_worker = User.objects.create(password='worker_super_ps_387', username='cu_api_test_worker_1',
                                              type=User.UserType.WORKER, photo=cls.image_creator.get_fake_image())

        cls.other_customer = cls.user_customer.customer
        cls.customer = cls.user.customer
        customer = cls.customer
        worker = cls.user_worker.worker
        cls.other_customer_task = Task.objects.create(title='Customer test task_1 (wait)', customer=cls.other_customer)
        cls.task = Task.objects.create(title='Customer test task_1 (wait)', customer=customer)
        cls.task_in_process_1 = Task.objects.create(title='Customer test task_1 (in_process)',
                                                    status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_in_process_2 = Task.objects.create(title='Customer test task_2 (in_process)',
                                                    status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_done = Task.objects.create(title='Customer worker test task_3 (done)',
                                            status=Task.StatusType.IN_PROCESS,
                                            customer=customer, worker=worker)

        cls.task_done.report = 'test'
        cls.task_done.status = Task.StatusType.DONE
        cls.task_done.save()

    @classmethod
    def setUpTestUser(cls):
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='worker_test',
                                            phone='+375291850665',
                                            type='customer'
                                            )

    def setUp(self):
        super().setUp()

    def test_api_jwt(self):
        url = reverse('token_obtain_pair')
        auth = self.client.post(url,
                                {'username': self.user.username,
                                 'password': self.clean_password},
                                format='json')

        self.assertEqual(auth.status_code, status.HTTP_200_OK)

    def test_get_list(self):
        customer_id = self.customer.id
        url = reverse('tasks-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_list = response.data
        task_query_length = Task.objects.filter(customer=customer_id).count()
        self.assertEqual(len(task_list), task_query_length)
        self.assertEqual(len(task_list), 4)

        for task in task_list:
            with self.subTest(task=task):
                self.assertEqual(task['customer'], customer_id)

    def test_get_list_search(self):
        data = {'search': 'done'}
        url = reverse('tasks-list')
        response = self.client.get(url, data=data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_list = response.data
        task_query_length = Task.objects.filter(
            Q(customer=self.customer.id) & (
                    Q(title__contains=data['search']) | Q(status__contains=data['search'])
            )
        ).count()
        self.assertEqual(len(task_list), task_query_length)
        self.assertEqual(len(task_list), 1)

        for task in task_list:
            with self.subTest(task=task):
                search_place = task['title'] + task['status']
                self.assertRegex(search_place.lower(), 'done')

    def test_get_list_other_customer(self):
        url = reverse('tasks-list') + f'?customer={self.other_customer.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_detail_customer_task(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_other_customer_task(self):
        url = reverse('tasks-detail', args=(self.other_customer_task.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_task(self):
        url = reverse('tasks-take-in-process', args=(self.task,))
        data = {'title': 'new_title'}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        data = {'title': 'new_title'}
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(data['title'], self.task.title)

    def test_patch(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        data = {'title': 'new_title'}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_put_running_task(self):
        url = reverse('tasks-detail', args=(self.task_in_process_2.id,))
        data = {'title': 'new_title'}
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        url = reverse('tasks-list')
        data = {
            "title": "test_task"
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer'], self.customer.id)

    def test_post_with_other_customer_id(self):
        url = reverse('tasks-list')
        data = {
            "title": "test_task",
            'customer': self.other_customer.id
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['customer'], data['customer'])

    def test_delete(self):
        url = reverse('tasks-detail', args=(self.task_in_process_2.id,))
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
