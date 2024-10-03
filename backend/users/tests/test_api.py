from django.conf import settings
from django.urls import reverse
from rest_framework import status

from services.APITestCaseWithJWT import APITestCaseWithJWT
from services.mixins.tests import ImageCreator, get_temp_file
from users.models import User


class SuperWorkerUsersAPITestCase(ImageCreator, APITestCaseWithJWT):
    """Тестирование запросов заказчика"""
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
                                            type='worker',
                                            photo=worker_photo,
                                            is_staff=True
                                            )

    def setUp(self):
        super().setUp()

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
            'photo': self.image_creator.get_fake_image()
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(str(data['photo'])[:-4], response.data['photo'])
