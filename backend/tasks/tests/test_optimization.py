from django.conf import settings
from django.urls import reverse

from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from services.APITestCaseWithJWT import APITestCaseWithJWT
from users.models import User, Customer
from tasks.models import Task


class SuperWorkerTaskAPITestCase(APITestCaseWithJWT):
    """Тестирование запросов работника с привилегиями"""
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
        print('\nOptimization test:')
        cls.customer = Customer.objects.last()

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
            self.client.get(url)

    def test_get_task(self):
        url = reverse('tasks-detail', args=(61,))
        with self.assertNumQueries(2):
            self.client.get(url)

    def test_post_task(self):
        url = reverse('tasks-list')
        data = {
            "title": "test_task",
            'customer': 6
        }

        with self.assertNumQueries(3):
            self.client.post(url, data=data)