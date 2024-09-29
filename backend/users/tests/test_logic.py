from django.test import TestCase
from django.conf import settings

# Create your tests here.

from users.models import User
from users.tests.utils import get_temp_file, open_photo_file, close_photo_file


class UserTestCase(TestCase):
    """Тестирование бизнесс-логики авторизация приложения"""

    fixtures = [
        'users/tests/fixtures/only_users_backup.json',
        'users/tests/fixtures/customers_data_backup.json', 'users/tests/fixtures/workers_data_backup.json',
        'tasks/tests/fixtures/task_test_backup.json'
    ]

    @classmethod
    def setUpTestData(cls):
        print('\nUser business-logic test:')
        cls.user_last_customer = User.objects.filter(type=User.UserType.CUSTOMER).last()
        cls.user_last_worker = User.objects.filter(type=User.UserType.WORKER).last()
        cls.photo_path = 'users/tests/data/img.png'

    def setUp(self):
        settings.MEDIA_ROOT = get_temp_file()

    def test_create_default_user(self):
        user_customer = User.objects.create_user(password='customer_super_ps_387',
                                                 username='customer_test_1',
                                                 phone='+375291850665'
                                                 )
        user_customer.refresh_from_db()
        user_customer.save()
        self.assertIn('pbkdf2_sha256', user_customer.password)
        self.assertTrue(hasattr(user_customer, User.UserType.CUSTOMER))

    def test_create_worker_user(self):
        user_worker = User.objects.create_user(password='customer_worker_ps_387',
                                               username='worker_test_1',
                                               phone='+375291850665',
                                               type=User.UserType.WORKER
                                               )
        user_worker.refresh_from_db()
        user_worker.save()
        self.assertIn('pbkdf2_sha256', user_worker.password)
        self.assertTrue(hasattr(user_worker, User.UserType.WORKER))

    def test_change_user_data(self):
        name = 'vasya stypin'
        self.user_last_worker.username = name
        self.user_last_worker.save()
        self.assertEqual(self.user_last_worker.username, name)

    def test_create_user(self):
        mem_file = open_photo_file(self.photo_path)
        user_worker = User.objects.create_user(password='customer_worker_ps_387',
                                               username='worker_test_with_photo',
                                               phone='+375291850665',
                                               type=User.UserType.WORKER,
                                               photo=mem_file
                                               )
        close_photo_file(mem_file)
        self.assertEqual('users/2024/09/28/img_2.png', user_worker.photo)

    #
    # def test_change_user_type(self):
    #     user_customer = User.objects.filter(type=User.UserType.CUSTOMER).last()
    #     user_customer.type = User.UserType.WORKER
    #     self.assertRaisesRegex(
    #         ValidationError,
    #         r'Пользователь .* уже имеет тип!',
    #         user_customer.save
    #     )
    #
    # def test_create_worker(self):
    #     self.assertRaisesRegex(
    #         utils.IntegrityError,
    #         r'NOT NULL constraint failed:',
    #         Worker.objects.create
    #     )
    #
    # def test_create_customer(self):
    #     self.assertRaisesRegex(
    #         utils.IntegrityError,
    #         r'NOT NULL constraint failed:',
    #         Customer.objects.create
    #     )
    #
    # def test_change_user_role_data(self):
    #     self.assertRaisesRegex(
    #         utils.IntegrityError,
    #         r'UNIQUE constraint failed',
    #         Worker.objects.create,
    #         user=self.user_last_worker
    #     )
    #
    # def test_create_worker_user_with_customer_data(self):
    #     self.assertRaisesRegex(
    #         ValidationError,
    #         r'Пользователь .* является \bworker\b|\bcustomer\b и вы не можете назначить ему тип .*',
    #         Customer.objects.create,
    #         user=self.user_last_worker
    #     )
    #
    # def test_create_customer_user_with_worker_data(self):
    #     self.assertRaisesRegex(
    #         ValidationError,
    #         r'Пользователь .* является \bworker\b|\bcustomer\b и вы не можете назначить ему тип .*',
    #         Worker.objects.create,
    #         user=self.user_last_customer
    #     )
