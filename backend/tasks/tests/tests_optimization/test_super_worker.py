import json

from django.conf import settings
from django.urls import reverse
from rest_framework import status

from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from services.APITestCaseWithJWT import APITestCaseWithJWT
from users.models import User, Customer
from tasks.models import Task


class SuperWorkerOptimizationTestCase(APITestCaseWithJWT):
    """Тестирование запросов работника с привилегиями"""
    image_creator = ImageCreator

    @classmethod
    def setUpTestData(cls):
        settings.MEDIA_ROOT = get_temp_file()
        super().setUpTestData()
        print('\nSuper-worker optimization test:')
        cls.user_customer = User.objects.create_user(password=cls.clean_password, username='customer_optimization_test')
        cls.customer = cls.user_customer.customer
        cls.worker = cls.user.worker
        cls.task = Task.objects.create(title='Customer test task_1 (wait)', customer=cls.customer)
        cls.task_in_process = Task.objects.create(title='Customer test task_1 (in_process)',
                                                  status=Task.StatusType.IN_PROCESS,
                                                  customer=cls.customer, worker=cls.worker)

    @classmethod
    def setUpTestUser(cls):
        worker_photo = cls.image_creator.get_fake_image()
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='super_worker_test_1',
                                            phone='+375291850665',
                                            type='worker',
                                            photo=worker_photo,
                                            is_staff=True
                                            )

    def test_get_all_tasks(self):
        url = reverse('tasks-list')
        with self.assertNumQueries(2):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        with self.assertNumQueries(2):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_task(self):
        url = reverse('tasks-list')
        data = {
            "title": "test_task",
            'customer': self.customer.id
        }

        with self.assertNumQueries(3):
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_take_wait_task_in_process(self):
        url = reverse('tasks-take-in-process', args=(self.task.id,))

        with self.assertNumQueries(4):
            response = self.client.patch(url, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_done_task(self):
        url = reverse('tasks-done', args=(self.task_in_process.id,))

        with self.assertNumQueries(3):
            data = {'report': 'test'}
            json_data = json.dumps(data)
            response = self.client.patch(url, data=json_data,
                                         content_type='application/json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)


