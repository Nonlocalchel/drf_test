from django.conf import settings
from django.test import TestCase

from services.mixins.tests import ManipulateExpectedDataMixin
from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from users.models import User
from users.serializers import UserSerializer
from users.utils.serializer_utils import format_repr


class SerializerTestCase(ManipulateExpectedDataMixin, TestCase):
    """Testing user app serializer"""

    image_creator = ImageCreator
    expected_data_path = "users/tests/data/expected_data.json"

    @classmethod
    def setUpTestData(cls):
        print('\nUser Serializer test:')
        settings.MEDIA_ROOT = get_temp_file()
        cls.user_customer = User.objects.create(password='customer_super_ps_387', username='serializer_test_customer_1')
        cls.user_worker = User.objects.create(password='worker_super_ps_387', username='serializer_test_worker_1',
                                              type=User.UserType.WORKER, photo=cls.image_creator.get_fake_image())
        cls.worker = cls.user_worker.worker
        cls.customer = cls.user_customer.customer

    def setUp(self):
        if not hasattr(self, 'worker'):
            self.setUpTestData()

    def test_read_one_user_data_serializer(self):
        """Get one user data(retrieve)"""
        instance = User.objects.get(worker=self.worker.id)
        serializer = UserSerializer(instance)
        serialized_data = serializer.data
        expected_data = self.get_expected_data()
        serialized_data['pk'] = expected_data['pk']
        serialized_data['photo'] = expected_data['photo']
        serialized_data['profile_data']['pk'] = expected_data['profile_data']['pk']
        self.assertEqual(serialized_data, expected_data)

    def test_create_user_serializer(self):
        """Create user data"""
        data = {
            'username': 'customer_21',
            'phone': '+375 29 485 06 33',
            'password': 'aga',
            'photo': None,
            'type': 'customer',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_superuser': False,
            'worker': None,
            'customer': {
                'discount': 26,
                'legal': 'person'
            }
        }

        serializer_post = UserSerializer(data=data)
        serializer_post.is_valid(raise_exception=True)
        del data['password']
        data = format_repr(data, User.UserType.CUSTOMER)
        self.assertEqual(serializer_post.data, data)
