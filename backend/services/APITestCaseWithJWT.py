from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User


class APITestCaseWithJWT(APITestCase):
    """Extending the Base class to get a JWT access token"""
    clean_password = None
    user = None

    @classmethod
    def setUpTestData(cls):
        """Can be extended by overriding and calling super().setUpTestData() at the end"""
        cls.setUpTestUser()

    @classmethod
    def setUpTestUser(cls):
        """
        Method for creating a user.
        Called from setUpTestData.
        Needs to be overridden (for compatibility with your DB).
        """
        cls.clean_password = 'worker_super_ps_387'
        cls.user = User.objects.create_user(password=cls.clean_password, username='Test_1')

    def setUp(self):
        """Can be extended by overriding and calling super().setUp() at the end"""
        self.jwt_auth(user=self.user)

    def jwt_auth(self, user):
        """
        Method for assigning client header with JWT token
        Don't touch!!!
        """
        url = reverse('token_obtain_pair')
        auth = self.client.post(url,
                                {'username': user.username, 'password': self.clean_password},
                                format='json')

        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
