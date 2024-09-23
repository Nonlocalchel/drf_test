from django.db import utils
from django.test import TestCase

# Create your tests here.

from django.core.exceptions import ValidationError

from users.models import User, Customer, Worker


class UserTestCase(TestCase):
    """Тестирование бизнесс-логики авторизация приложения"""

    fixtures = ['test_users_backup.json', 'test_customer_backup.json',
                'test_worker_backup.json', 'test_tasks_backup.json']

    @classmethod
    def setUpTestData(cls):
        print('\nUser test:')

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
        user_worker = User.objects.create_user(password='customer_super_ps_387',
                                               username='customer_test_1',
                                               phone='+375291850665',
                                               type=User.UserType.WORKER
                                               )
        user_worker.refresh_from_db()
        user_worker.save()
        self.assertIn('pbkdf2_sha256', user_worker.password)
        self.assertTrue(hasattr(user_worker, User.UserType.WORKER))

    def test_change_user_type(self):
        user_customer = User.objects.filter(type=User.UserType.CUSTOMER).last()
        user_customer.type = User.UserType.WORKER
        self.assertRaisesRegex(
            ValidationError,
            r'Пользователь .* уже имеет тип!',
            user_customer.save
        )

    def test_create_worker(self):
        self.assertRaisesRegex(
            utils.IntegrityError,
            r'NOT NULL constraint failed:',
            Worker.objects.create
        )

    def test_create_customer(self):
        self.assertRaisesRegex(
            utils.IntegrityError,
            r'NOT NULL constraint failed:',
            Customer.objects.create
        )

    def test_add_user_role_data(self):
        user_worker = User.objects.filter(type=User.UserType.WORKER).last()
        user_worker.customer = Customer.objects.create(user=user_worker)
        self.assertRaisesRegex(
            ValidationError,
            r'Пользователь .* является \bworker\b|\bcustomer\b',
            user_worker.save
        )

    def test_change_user_role_data(self):
        user_worker = User.objects.filter(type=User.UserType.WORKER).last()
        self.assertRaisesRegex(
            utils.IntegrityError,
            r'UNIQUE constraint failed',
            Worker.objects.create,
            user=user_worker
        )
