import json

from django.conf import settings
from django.urls import reverse

from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from services.APITestCaseWithJWT import APITestCaseWithJWT
from users.models import User, Customer
from tasks.models import Task


class WorkerOptimizationTestCase(APITestCaseWithJWT):
    """Testing worker optimization"""
    image_creator = ImageCreator

    @classmethod
    def setUpTestData(cls):
        settings.MEDIA_ROOT = get_temp_file()
        super().setUpTestData()
        print('\nWorker optimization test:')
        cls.customer = Customer.objects.last()
        cls.task_wait = Task.objects.filter(status=Task.StatusType.WAIT)[0]
        cls.task_in_process = Task.objects.create(title='Worker test task_1 (in_process)',
                                                  status=Task.StatusType.IN_PROCESS,
                                                  customer=cls.customer, worker=cls.user.worker)

    @classmethod
    def setUpTestUser(cls):
        worker_photo = cls.image_creator.get_fake_image()
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='super_worker_test_1',
                                            phone='+375291850665',
                                            type='worker',
                                            photo=worker_photo
                                            )

    def test_get_all_tasks(self):
        """Get task list(1 request- auth + 1 request- task-list)"""
        url = reverse('tasks-list')
        with self.assertNumQueries(2):
            self.client.get(url)

    def test_get_task(self):
        """Get one task(1 request- auth + 1 request- task-list)"""
        url = reverse('tasks-detail', args=(61,))
        with self.assertNumQueries(2):
            self.client.get(url)

    def test_patch_take_wait_task_in_process(self):
        """Get one task(1 request- auth + 1 request- get task + 1 request select worker + 1 request update)"""
        url = reverse('tasks-take-in-process', args=(self.task_wait.id,))

        with self.assertNumQueries(4):
            self.client.patch(url, content_type='application/json')

    def test_done_task(self):
        """Get one task(1 request- auth + 1 request- get task + 1 request update)"""
        url = reverse('tasks-done', args=(self.task_in_process.id,))
        data = {'report': 'new'}
        json_data = json.dumps(data)

        with self.assertNumQueries(3):
            self.client.patch(url, data=json_data, content_type='application/json')
