import json

from django.urls import reverse
from rest_framework import status

from tasks.messages.validation_error import TaskValidationMessages
from tasks.models import Task
from tasks.tests.tests_api.test_jwt import APITestCaseWithJWT
from users.models import User, Customer


class SuperWorkerTaskAPITestCase(APITestCaseWithJWT):
    """Тестирование запросов работника с привилегиями"""

    fixtures = ['test_users_backup.json', 'test_customer_backup.json',
                'test_worker_backup.json', 'test_tasks_backup.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('\nSuper worker test:')
        worker = cls.user.worker
        cls.customer = Customer.objects.last()
        customer = cls.customer
        cls.task = Task.objects.create(title='Worker test task_1 (wait)', customer=customer)
        cls.task_in_process_1 = Task.objects.create(title='Super worker test task_1 (in_process)',
                                                    status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_in_process_2 = Task.objects.create(title='Super worker test task_2 (in_process)',
                                                    status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_done = Task.objects.create(title='Super worker test task_3 (done)', status=Task.StatusType.IN_PROCESS,
                                            customer=customer, worker=worker)

        cls.task_done.report = 'test'
        cls.task_done.status = Task.StatusType.DONE
        cls.task_done.save()

    @classmethod
    def setUpTestUser(cls):
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='super_worker_test_1',
                                            phone='+375291850665',
                                            type='worker'
                                            )

        cls.user.worker.is_super_worker = True
        cls.user.worker.save()

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
        url = reverse('tasks-list') + f'?worker={self.user.id},null'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_other_worker(self):
        url = reverse('tasks-list') + f'?worker=37'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_all(self):
        url = reverse('tasks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_nobody_task(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_worker_task(self):
        url = reverse('tasks-detail', args=(self.task_in_process_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_other_worker(self):
        url = reverse('tasks-detail', args=(61,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_patch_take_process_task_in_process(self):
        url = reverse('tasks-detail', args=(61,))
        data = {'status': Task.StatusType.IN_PROCESS}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        validation_message = response.data['report'][0]
        self.assertEqual(validation_message, TaskValidationMessages.EMPTY_REPORT_ERROR)

    def test_patch_done_task(self):
        url = reverse('tasks-detail', args=(self.task_done.id,))
        data = {'report': 'test23435467'}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        validation_message = response.data['status'][0]
        self.assertEqual(validation_message, TaskValidationMessages.CHANGE_DONE_TASK_ERROR)

    def test_put(self):
        url = reverse('tasks-detail', args=(self.task_in_process_2.id,))
        data = {'title': 'new_title'}
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        url = reverse('tasks-list')
        data = {
            "title": "test_task",
            'customer': self.customer.user.id
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_without_customer(self):
        url = reverse('tasks-list')
        data = {
            "title": "test_task"
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.data['customer'].pop()
        self.assertEqual(error_message, 'Обязательное поле.')
