from django.test import TestCase

# Create your tests here.

from django.core.exceptions import ValidationError

from users.models import User


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
        try:
            user_customer = User.objects.filter(type=User.UserType.CUSTOMER).last()
            user_customer.type = User.UserType.WORKER
            user_customer.save()
            self.assertEqual(12, 2)
        except ValidationError as validation_error:
            message = dict(validation_error)['type'][0]
            self.assertRegex(message, 'Пользователь .* уже имеет тип!')

        # self.assertIn('pbkdf2_sha256', user.password)
        # user.refresh_from_db()
        # user.save()
        # user.type = User.UserType.CUSTOMER
        # user.refresh_from_db()
        # user.save()
        # print(user.type)
