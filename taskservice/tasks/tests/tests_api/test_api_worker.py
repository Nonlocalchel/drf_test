import json

from django.urls import reverse
from rest_framework import status

from tasks.models import Task
from tasks.tests.tests_api.test_api_jwt import APITestCaseWithJWT
from users.models import User, Customer


class WorkerTaskAPITestCase(APITestCaseWithJWT):
    """Тестирование запросов работника"""

    fixtures = ['test_users_backup.json', 'test_customer_backup.json',
                'test_worker_backup.json', 'test_tasks_backup.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        worker = cls.user.worker
        customer = Customer.objects.last()
        cls.task = Task.objects.create(title='Test task_1 (wait)', customer=customer)
        cls.task_in_process_1 = Task.objects.create(title='Test task_1 (in_process)', status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_in_process_2 = Task.objects.create(title='Test task_2 (in_process)', status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_done = Task.objects.create(title='Test task_3 (done)', status=Task.StatusType.IN_PROCESS,
                                            customer=customer, worker=worker)

        cls.task_done.report = 'test'
        cls.task_done.status = Task.StatusType.DONE
        cls.task_done.save()  # т.к. по другому (пр. cls.task_done.time_close = cls.task_done.time_update)
        # время не созраняются

    @classmethod
    def setUpTestUser(cls):
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='Test_1',
                                            phone='+375291850665',
                                            type='worker'
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
        url = reverse('tasks-detail', args=(self.task.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_fail(self):
        url = reverse('tasks-detail', args=(61,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_take_wait_task_in_process(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        data = {'status': Task.StatusType.IN_PROCESS}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.task.refresh_from_db()
        self.assertEqual(self.user.worker, self.task.worker)
        self.assertEqual(Task.StatusType.IN_PROCESS, self.task.status)

    def test_patch_done(self):
        url = reverse('tasks-detail', args=(self.task_in_process_1.id,))
        data = {'status': Task.StatusType.DONE,
                'report': 'test'
                }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        task_data = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.task.refresh_from_db()
        self.assertEqual(self.user.id, task_data['worker'])
        self.assertEqual(Task.StatusType.DONE, task_data['status'])

    def test_patch_done_without_report(self):
        url = reverse('tasks-detail', args=(self.task_in_process_2.id,))
        data = {'status': Task.StatusType.DONE}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_patch_done_task(self):
        url = reverse('tasks-detail', args=(self.task_done.id,))
        data = {'report': 'test23435467'}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)



    # @unittest.expectedFailure
    # def test_patch_take_process_task_in_process(self):
    #     url = reverse('tasks-detail', args=(self.task_in_process_1.id,))
    #     data = {'status': Task.StatusType.IN_PROCESS}
    #     json_data = json.dumps(data)
    #     response = self.client.patch(url, data=json_data,
    #                                  content_type='application/json')
    #
    #     print(response.data)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)

    # def test_post(self):
    ## def test_put(self):