import json


from django.test import TestCase

from users.models import Worker, Customer, User
from users.serializers import UserSerializer


class SerializerTestCase(TestCase):
    """Тестирование сериализаторов приложения"""

    expected_data_path = "users/tests/expected_data.json"
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

    def setUp(self):
        if not hasattr(self, 'worker'):
            self.setUpTestData()

    def get_expected_data(self) -> list:
        path = self.expected_data_path
        with open(path) as expected_data_file:
            expected_data = json.loads(expected_data_file.read())
            return expected_data

    def write_data_to_json_file(self, new_data) -> None:
        path = self.expected_data_path
        with open(path, 'w') as expected_data_file:
            new_json_data = json.dumps(new_data)
            expected_data_file.write(new_json_data)

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

    @staticmethod
    def representation_expected_data(data: dict) -> dict:
        presentation_data = data
        presentation_data['pk'] = 76
        presentation_data['customer']['pk'] = 7
        del presentation_data['customer']['id']
        del presentation_data['password']
        return presentation_data

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
        test = serializer_post.save()
        self.assertEqual(test.username, data['username'])

        user = User.objects.get(username=data['username'])
        serializer_get = UserSerializer(user)
        expected_data = self.representation_expected_data(data)
        serialized_data = serializer_get.data
        self.assertEqual(serialized_data, expected_data)
