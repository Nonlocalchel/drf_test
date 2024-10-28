from django.conf import settings
from django.urls import reverse
from rest_framework import status

from services.APITestCaseWithJWT import APITestCaseWithJWT
from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from users.models import User


class SuperWorkerUsersAPITestCase(APITestCaseWithJWT):
    """Тестирование запросов данных пользователей работника с extra правами"""
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
        print('\nSuper worker tasks test:')

    @classmethod
    def setUpTestUser(cls):
        worker_photo = cls.image_creator.get_fake_image()
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='super_worker_test_1',
                                            phone='+375291850665',
                                            type=User.UserType.WORKER,
                                            photo=worker_photo,
                                            is_staff=True
                                            )

    def setUp(self):
        super().setUp()

    def test_api_jwt(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': self.user.username,
            'password': self.clean_password
        }
        auth = self.client.post(url, data)

        self.assertEqual(auth.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        url = reverse('users-list')
        data = {
            "username": "test_user_hz",
            'phone': '+23424904920',
            'password': 'super_ps',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_photo(self):
        url = reverse('users-list')
        data = {
            'password': 'sadfgh',
            'username': 'super_worker_test_123',
            'photo': self.image_creator.get_fake_image()
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(str(data['photo'])[:-4], response.data['photo'])

    def test_get_all_users(self):
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 9)

    def test_get_user_data(self):
        url = reverse('users-detail', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_user_data(self):
        url = reverse('users-detail', args=(75,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
