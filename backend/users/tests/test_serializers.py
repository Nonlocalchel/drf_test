from django.conf import settings
from django.test import TestCase

from services.mixins.tests import ManipulateExpectedDataMixin
from services.tests_utils import get_temp_file
from services.ImageWorker import ImageCreator
from users.models import Worker, Customer, User
from users.serializers import UserSerializer
from users.utils import format_repr


class SerializerTestCase(ManipulateExpectedDataMixin, TestCase):
    """Тестирование сериализаторов приложения"""

    image_creator = ImageCreator
    expected_data_path = "users/tests/data/expected_data.json"
    fixtures = [
        'users/tests/fixtures/only_users_backup.json',
        'users/tests/fixtures/workers_data_backup.json'
    ]

    @classmethod
    def setUpTestData(cls):
        print('\nUser Serializer test:')
        settings.MEDIA_ROOT = get_temp_file()
        cls.worker = Worker.objects.last()
        cls.customer = Customer.objects.last()
        cls.photo_path = 'users/tests/data/img.png'

    def setUp(self):
        if not hasattr(self, 'worker'):
            self.setUpTestData()

    def test_read_all_users_data_serializer(self):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        serialized_data = serializer.data
        # self.write_data_to_json_file(serialized_data)
        expected_data = self.get_expected_data()
        self.assertEqual(expected_data, serialized_data)

    def test_read_one_user_data_serializer(self):
        instance = User.objects.get(worker=self.worker.id)
        serializer = UserSerializer(instance)
        serialized_data = serializer.data
        expected_data = self.get_expected_data()
        self.assertEqual(serialized_data, expected_data[4])

    def test_create_user_serializer(self):
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
