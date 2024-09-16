from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User


class APITestCaseWithJWT(APITestCase):
    """Расширение Базового класса для получения JWT access-token"""
    clean_password = None
    user = None

    @classmethod
    def setUpTestData(cls):
        """
        Можно расширять,переопределив и вызвав в конце super().setUpTestData()
        """
        cls.setUpTestUser()

    @classmethod
    def setUpTestUser(cls):
        """
        Метод для создания пользователя
        Вызывается из setUpTestData
        Нужно переопределять(для совместимости с вашей БД)
        """
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password, username='Test_1')

    def setUp(self):
        """
        Можно расширять,переопределив и вызвав в конце super().setUp()
        """
        self.jwt_auth(user=self.user)

    def jwt_auth(self, user):
        """
        Метод для наделения client заголовком с JWT токеном
        Не трогать!!!
        """
        url = reverse('token_obtain_pair')
        auth = self.client.post(url,
                                {'username': user.username, 'password': self.clean_password},
                                format='json')

        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
