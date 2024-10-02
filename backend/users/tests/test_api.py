from django.urls import reverse
from rest_framework import status

from services.APITestCaseWithJWT import APITestCaseWithJWT
from services.mixins.tests import ImageCreator
from users.models import User


class SuperWorkerUsersAPITestCase(ImageCreator, APITestCaseWithJWT):
    """Тестирование запросов заказчика"""

    fixtures = [
        'users/tests/fixtures/only_users_backup.json',
        'users/tests/fixtures/customers_data_backup.json', 'users/tests/fixtures/workers_data_backup.json',
        'tasks/tests/fixtures/task_test_backup.json'
    ]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('\nSuper worker tasks test:')
        cls.photo_path = 'users/tests/data/img.png'

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
        self.set_media_root()

    def test_api_jwt(self):
        url = reverse('token_obtain_pair')
        auth = self.client.post(url,
                                {'username': self.user.username,
                                 'password': self.clean_password}
                                )

        self.assertEqual(auth.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        url = reverse('users-list')
        data = {
            "username": "test_user_hz",
            'password': 'super_ps'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_photo(self):
        url = reverse('users-list')
        data = {
            'password': 'sadfgh',
            'username': 'super_worker_test_123',
            'photo': self.get_fake_image
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)
