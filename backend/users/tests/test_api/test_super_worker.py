import json

from django.conf import settings
from django.urls import reverse
from rest_framework import status

from services.APITestCaseWithJWT import APITestCaseWithJWT
from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from users.models import User, Customer


class SuperWorkerUsersAPITestCase(APITestCaseWithJWT):
    """Тестирование запросов данных пользователей работника с extra правами"""
    image_creator = ImageCreator

    @classmethod
    def setUpTestData(cls):
        settings.MEDIA_ROOT = get_temp_file()
        super().setUpTestData()
        print('\nSuper worker user test:')
        cls.other_customer = User.objects.create_user(password='customer_super_ps_387', username='sw_test_customer_1')
        cls.other_worker = User.objects.create_user(password='worker_super_ps_387', username='sw_test_worker_1',
                                                    type=User.UserType.WORKER, photo=cls.image_creator.get_fake_image())

    @classmethod
    def setUpTestUser(cls):
        worker_photo = cls.image_creator.get_fake_image()
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='user_worker_super_worker_test',
                                            phone='+375291850665',
                                            type=User.UserType.WORKER,
                                            photo=worker_photo,
                                            is_staff=True
                                            )

    def setUp(self):
        super().setUp()

    def test_api_jwt(self):
        """Authorized with user jwt"""
        url = reverse('token_obtain_pair')
        data = {
            'username': self.user.username,
            'password': self.clean_password
        }
        auth = self.client.post(url, data)

        self.assertEqual(auth.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """Create user"""
        url = reverse('users-list')
        data = {
            "username": "test_user_hz",
            'phone': '+23424904920',
            'password': 'super_ps',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_only_password_and_username(self):
        """Create user with only password and username"""
        url = reverse('users-list')
        data = {
            "username": "test_user_hz",
            'password': 'super_ps',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_only_password(self):
        """Create user with only password"""
        url = reverse('users-list')
        data = {
            'password': 'super_ps',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_only_username(self):
        """Create user with only username"""
        url = reverse('users-list')
        data = {
            "username": "test_user_hz"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_photo(self):
        """Create user with photo"""
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
        """Get users list"""
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)

    def test_get_user_data(self):
        """Get user"""
        url = reverse('users-detail', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_user_data(self):
        """Get other user"""
        url = reverse('users-detail', args=(self.other_customer.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_with_nested_data(self):
        url = reverse('users-list')
        data = {
            'username': 'new_customer',
            'phone': '341 8 7698-1576-189 9888 55',
            'photo': self.image_creator.get_fake_image(),
            'type': 'customer',
            'worker': json.dumps({
                'exp': 92233600,
                'speciality': 'string',
                'education': 'string'
            }),
            'customer': json.dumps({
                'discount': 9223770,
                'legal': 'entity'
            }),
            'password': 'string'
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(str(data['photo'])[:-4], response.data['photo'])