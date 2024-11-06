import json

from django.urls import reverse
from rest_framework import status

from services.APITestCaseWithJWT import APITestCaseWithJWT
from services.ImageWorker import ImageCreator
from tasks.models import Task
from users.models import User


class CustomerOptimizationTestCase(APITestCaseWithJWT):
    """Тестирование запросов работника с привилегиями"""
    image_creator = ImageCreator

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('\nCustomer optimization test:')
        cls.customer = cls.user.customer
        cls.user_worker = User.objects.create(password='worker_super_ps_387', username='cu_optimization_test_worker_1',
                                              type=User.UserType.WORKER, photo=cls.image_creator.get_fake_image())

        customer = cls.customer
        worker = cls.user_worker.worker
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
        cls.clean_password = 'customer_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='customer_optimization_test',
                                            phone='+375291850665',
                                            type='customer'
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
            "title": "test_task"
        }
        json_data = json.dumps(data)

        with self.assertNumQueries(3):
            response = self.client.post(url, data=json_data,
                                        content_type='application/json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
