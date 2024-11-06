from django.urls import reverse
from rest_framework import status

from services.APITestCaseWithJWT import APITestCaseWithJWT
from users.messages.permission_denied import UserPermissionMessages
from users.models import User


class SuperCustomerUsersAPITestCase(APITestCaseWithJWT):
    """Тестирование запросов данных пользователей заказчика c extra правами"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('\nSuper customer tasks test:')

    @classmethod
    def setUpTestUser(cls):
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password,
                                            username='super_worker_test_1',
                                            phone='+375291850665',
                                            is_staff=True
                                            )

    def setUp(self):
        super().setUp()

    def test_api_jwt(self):
        """Authorized with user jwt"""
        url = reverse('token_obtain_pair')
        auth = self.client.post(url,
                                {'username': self.user.username,
                                 'password': self.clean_password}
                                )

        self.assertEqual(auth.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """Create user"""
        url = reverse('users-list')
        data = {
            "username": "test_user_hz",
            'password': 'super_ps'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], str(UserPermissionMessages.SUPER_WORKER_ACCESS))

    def test_get_all_users(self):
        """Get users list"""
        url = reverse('users-list')
        response = self.client.get(url)
        users_list = response.data
        self.assertEqual(len(users_list), 2)

        for user in users_list:
            with self.subTest(user=user):
                user_type = user['type']
                self.assertEqual(user_type, User.UserType.WORKER)

    def test_get_customer_users(self):
        """Get users list with type customer"""
        data = {
            'type': User.UserType.CUSTOMER
        }
        url = reverse('users-list')
        response = self.client.get(url, data=data)
        self.assertEqual(response.data, [])

    def test_get_user_data(self):
        """Get user"""
        url = reverse('users-detail', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_user_data(self):
        """Get other user with type customer"""
        url = reverse('users-detail', args=(75,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_worker_user(self):
        """Get other user with type worker"""
        url = reverse('users-detail', args=(56,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
