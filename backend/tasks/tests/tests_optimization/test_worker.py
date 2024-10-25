from django.conf import settings
from django.urls import reverse

from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from services.APITestCaseWithJWT import APITestCaseWithJWT
from users.models import User, Customer
from tasks.models import Task


class SuperWorkerTaskAPITestCase(APITestCaseWithJWT):
    image_creator = ImageCreator
    fixtures = [
        'users/tests/fixtures/only_users_backup.json',
        'users/tests/fixtures/customers_data_backup.json', 'users/tests/fixtures/workers_data_backup.json',
        'tasks/tests/fixtures/task_test_backup.json'
    ]

    @classmethod
    def setUpTestData(cls):
        settings.MEDIA_ROOT = get_temp_file()
        super().setUpTestData()
        print('\nSuper-worker optimization test:')
        cls.customer = Customer.objects.last()
        cls.task_wait = Task.objects.filter(status=Task.StatusType.WAIT)[0]
        cls.task_in_process = Task.objects.filter(status=Task.StatusType.IN_PROCESS)[0]

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
        url = reverse('tasks-list')
        with self.assertNumQueries(3):
            self.client.get(url)

    def test_get_task(self):
        url = reverse('tasks-detail', args=(61,))
        with self.assertNumQueries(3):
            self.client.get(url)

    def test_patch_take_wait_task_in_process(self):
        url = reverse('tasks-take-in-process', args=(self.task_wait.id,))

        with self.assertNumQueries(5):
            self.client.patch(url, content_type='application/json')

    def test_done_task(self):
        url = reverse('tasks-done', args=(self.task_in_process.id,))

        with self.assertNumQueries(3):
            self.client.patch(url, content_type='application/json')
