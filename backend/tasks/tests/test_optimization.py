from django.conf import settings
from django.db import connection
from django.urls import reverse
from rest_framework import status

from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from services.APITestCaseWithJWT import APITestCaseWithJWT
from users.models import User


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
        print('\nSuper worker task test:')

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

    def test_get_list_of_two_workers(self):
        url = reverse('tasks-list')

        with self.assertNumQueries(2):
            response = self.client.get(url)
