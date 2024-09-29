from django.test import TestCase

from services.mixins.tests import ManipulateExpectedDataMixin
from users.models import Worker, Customer, User
from users.serializers import UserSerializer


class SerializerTestCase(ManipulateExpectedDataMixin, TestCase):
    """Тестирование сериализаторов приложения"""

    expected_data_path = "users/tests/data/expected_data.json"
    fixtures = [
        'users/tests/fixtures/only_users_backup.json',
        'users/tests/fixtures/customers_data_backup.json', 'users/tests/fixtures/workers_data_backup.json',
        'tasks/tests/fixtures/task_test_backup.json'
    ]

    @classmethod
    def setUpTestData(cls):
        print('\nUser Serializer test:')
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
            'username': 'customer_225',
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
                'is_super_customer': False
            }
        }

        serializer_post = UserSerializer(data=data)
        serializer_post.is_valid(raise_exception=True)
        del data['password']
        self.assertEqual(serializer_post.data, data)

    # def test_create_user_with_photo_serializer(self):
    #     user_photo = open_photo_file(self.photo_path)
    #     data = {
    #         'username': 'customer_225',
    #         'phone': '+375 29 485 06 33',
    #         'password': 'aga',
    #         'photo': user_photo,
    #         'type': 'customer',
    #         'email': '',
    #         'first_name': '',
    #         'last_name': '',
    #         'is_superuser': False,
    #         'worker': None,
    #         'customer': {
    #             'discount': 26,
    #             'is_super_customer': False
    #         }
    #     }
    #
    #     serializer_post = UserSerializer(data=data)
    #     print(serializer_post.initial_data)
    #     serializer_post.is_valid(raise_exception=True)
    #     del data['password']
    #     print(serializer_post.data)
    #     print(data)
    #     self.assertEqual(serializer_post.data, data)
    #     user_photo.close()

