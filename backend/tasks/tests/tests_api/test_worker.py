import json

from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from rest_framework import status

from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from tasks.messages.validation_error import TaskValidationMessages
from tasks.models import Task
from services.APITestCaseWithJWT import APITestCaseWithJWT
from users.models import User, Customer


class WorkerTaskAPITestCase(APITestCaseWithJWT):
    """Тестирование запросов работника"""
    image_creator = ImageCreator

    @classmethod
    def setUpTestData(cls):
        settings.MEDIA_ROOT = get_temp_file()
        super().setUpTestData()
        print('\nWorker tasks test:')
        cls.worker = cls.user.worker
        worker = cls.worker
        cls.customer = Customer.objects.last()
        customer = cls.customer
        cls.task = Task.objects.create(title='Test task_1 (wait)', customer=customer)
        cls.task_in_process_1 = Task.objects.create(title='Worker test task_1 (in_process)',
                                                    status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_in_process_2 = Task.objects.create(title='Worker test task_2 (in_process)',
                                                    status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_done = Task.objects.create(title='Worker test task_3 (done)', status=Task.StatusType.IN_PROCESS,
                                            customer=customer, worker=worker)

        cls.task_done.report = 'test'
        cls.task_done.status = Task.StatusType.DONE
        cls.task_done.save()

    @classmethod
    def setUpTestUser(cls):
        worker_photo = cls.image_creator.get_fake_image()
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='worker_test_1',
                                            phone='+375291850665',
                                            type='worker',
                                            photo=worker_photo
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
        worker_id = self.worker.id
        url = reverse('tasks-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_list = response.data
        task_query_length = Task.objects.filter(Q(worker=worker_id) | Q(worker__isnull=True)).count()
        self.assertEqual(len(task_list), task_query_length)
        self.assertEqual(6, len(task_list))

        for task in task_list:
            with self.subTest(task=task):
                worker = task['worker']
                self.assertIn(worker, [worker_id, None])

    def test_get_list_search(self):
        worker_id = self.worker.id
        data = {'search': 'done'}
        url = reverse('tasks-list')
        response = self.client.get(url, data=data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task_list = response.data
        task_query_length = Task.objects.filter(
            Q(worker=worker_id) & (
                    Q(title__contains=data['search']) | Q(status__contains=data['search'])
            )
        ).count()
        self.assertEqual(len(task_list), task_query_length)

        for task in task_list:
            with self.subTest(task=task):
                search_place = task['title'] + task['status']
                self.assertRegex(search_place.lower(), 'done')

    def test_get_list_other_worker(self):
        url = reverse('tasks-list') + f'?worker=1'
        response = self.client.get(url)
        empty_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(empty_data), 0)

    def test_get_detail_nobody_task(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_worker_task(self):
        url = reverse('tasks-detail', args=(self.task_in_process_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_other_worker(self):
        url = reverse('tasks-detail', args=(27,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_take_wait_task_in_process(self):
        url = reverse('tasks-take-in-process', args=(self.task.id,))
        response = self.client.patch(url, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.task.refresh_from_db()
        self.assertEqual(self.user.worker, self.task.worker)
        self.assertEqual(Task.StatusType.IN_PROCESS, self.task.status)

    def test_patch_by_main_url(self):
        url = reverse('tasks-detail', args=(self.task.id,))
        data = {'status': Task.StatusType.IN_PROCESS}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_patch_done(self):
        url = reverse('tasks-done', args=(self.task_in_process_1.id,))
        data = {'report': 'test'}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        task_data = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.task.refresh_from_db()
        self.assertEqual(self.worker.id, task_data['worker'])
        self.assertEqual(Task.StatusType.DONE, task_data['status'])

    def test_patch_done_without_report(self):
        url = reverse('tasks-done', args=(self.task_in_process_2.id,))
        data = {'report': ''}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        validation_message = response.data['report'][0]
        self.assertEqual(validation_message, TaskValidationMessages.EMPTY_REPORT_ERROR)

    def test_patch_done_task(self):
        url = reverse('tasks-done', args=(self.task_done.id,))
        data = {'report': 'test23435467'}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_done_other_worker_task(self):
        url = reverse('tasks-done', args=(27,))
        data = {'report': 'test23435467'}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
            "title": "test_task"
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        url = reverse('tasks-detail', args=(self.task_in_process_2.id,))
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
