import json

from django.conf import settings
from django.urls import reverse

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

    def test_get_all_users(self):
        url = reverse('users-list')

        with self.assertNumQueries(2):
            self.client.get(url)

    def test_get_user_account(self):
        url = reverse('users-detail', args=(self.user.id,))

        with self.assertNumQueries(1):
            self.client.get(url)

    def test_create_user(self):
        url = reverse('users-list')
        data = {
            'username': 'new_customer',
            'phone': '341 8 7698-1576-189 9888 55',
            'type': 'customer',
            # 'customer': {
            #     'discount': 9223372034776000,
            #     'legal': 'entity'
            # },
            'password': 'string'
        }

        with self.assertNumQueries(3):
            self.client.post(url, data=data, format='json')


'''
{
  "username": "enAbzk2Eojjsb0nQhjOWVVs+Vafjm7omrhqM21rINfHEk",
  "phone": "341 8 7698-1576-189 9888 55",
  "is_staff": true,
  "type": "customer",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "is_superuser": true,
  "worker": {
    "exp": 9223372036854776000,
    "speciality": "string",
    "education": "string"
  },
  "customer": {
    "discount": 9223372036854776000,
    "legal": "entity"
  },
  "password": "string"
}
'''
