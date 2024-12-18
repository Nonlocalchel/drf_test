from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import utils
from django.test import TestCase

from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
# Create your tests here.

from users.models import User, Worker, Customer


class UserTestCase(TestCase):
    """Testing business logic of user application"""
    image_creator = ImageCreator

    @classmethod
    def setUpTestData(cls):
        print('\nUser business-logic test:')
        settings.MEDIA_ROOT = get_temp_file()
        cls.user_customer = User.objects.create_user(password='customer_super_ps_387',
                                                     username='logic_test_customer_1',
                                                     phone='+375291850665'
                                                     )
        cls.user_worker = User.objects.create_user(password='worker_super_ps_387',
                                                   username='logic_test_worker_1',
                                                   phone='+375291850625',
                                                   type=User.UserType.WORKER,
                                                   photo=cls.image_creator.get_fake_image()
                                                   )

    def test_create_default_user(self):
        """Create default user"""
        user_customer = User.objects.create_user(password='customer_super_ps_387',
                                                 username='user_customer_bisuness-logic_test',
                                                 phone='+375291850335'
                                                 )
        user_customer.refresh_from_db()
        user_customer.save()
        self.assertIn('pbkdf2_sha256', user_customer.password)
        self.assertTrue(hasattr(user_customer, User.UserType.CUSTOMER))

    def test_create_worker_user(self):
        """Create worker user"""
        worker_photo = self.image_creator.get_fake_image()
        user_worker = User.objects.create_user(password='customer_worker_ps_387',
                                               username='worker_1',
                                               phone='+375291850633',
                                               type=User.UserType.WORKER,
                                               photo=worker_photo
                                               )
        user_worker.refresh_from_db()
        user_worker.save()
        self.assertIn('pbkdf2_sha256', user_worker.password)
        self.assertTrue(hasattr(user_worker, User.UserType.WORKER))

    def test_create_worker_user_without_photo(self):
        """Create worker user without photo"""
        self.assertRaisesRegex(
            ValidationError,
            r'Пользователь .* является работником и должен иметь фото!',
            User.objects.create_user,
            password='customer_worker_ps_387',
            username='worker_test_1',
            phone='+375221850678',
            type=User.UserType.WORKER
        )

    def test_change_user_data(self):
        """Change username"""
        name = 'vasya stypin'
        self.user_worker.username = name
        self.user_worker.save()
        self.assertEqual(self.user_worker.username, name)

    def test_create_worker_with_photo(self):
        """Create worker user"""
        user_photo = self.image_creator.get_fake_image()
        user_worker = User.objects.create_user(password='customer_worker_ps_387',
                                               username='worker_test_with_photo',
                                               phone='+375291850331',
                                               type=User.UserType.WORKER,
                                               photo=user_photo
                                               )
        self.assertIn('image2', user_worker.photo.path)

    def test_change_user_type(self):
        """Change user type"""
        user_customer = self.user_customer
        user_customer.type = User.UserType.WORKER
        self.assertRaisesRegex(
            ValidationError,
            r'Пользователь .* уже имеет тип!',
            user_customer.save
        )

    def test_create_worker(self):
        """Create profile worker data without user"""
        self.assertRaises(
            utils.IntegrityError,
            Worker.objects.create
        )

    def test_create_customer(self):
        """Create profile customer data without user"""
        self.assertRaises(
            utils.IntegrityError,
            Customer.objects.create
        )

    def test_change_user_role_data(self):
        """Change user profile data"""
        self.assertRaises(
            utils.IntegrityError,
            Worker.objects.create,
            user=self.user_worker
        )

    def test_create_worker_user_with_customer_data(self):
        """Change user profile data with other type"""
        self.assertRaisesRegex(
            ValidationError,
            r'Пользователь .* является \bworker\b|\bcustomer\b и вы не можете назначить ему тип .*',
            Customer.objects.create,
            user=self.user_worker
        )

    def test_create_customer_user_with_worker_data(self):
        """Change user profile data with other type"""
        self.assertRaisesRegex(
            ValidationError,
            r'Пользователь .* является \bworker\b|\bcustomer\b и вы не можете назначить ему тип .*',
            Worker.objects.create,
            user=self.user_customer
        )
