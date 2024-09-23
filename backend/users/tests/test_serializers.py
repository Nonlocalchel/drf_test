import json

from django.test import TestCase

from tasks.models import Task
from users.models import Worker, Customer, User
from users.serializers import UserSerializer


class SerializerTestCase(TestCase):
    """Тестирование сериализаторов приложения"""

    fixtures = ['test_users_backup.json', 'test_customer_backup.json',
                'test_worker_backup.json', 'test_tasks_backup.json']

    @classmethod
    def setUpTestData(cls):
        print('\nUser Serializer test:')
        cls.worker = Worker.objects.last()
        cls.customer = Customer.objects.last()

    def setUp(self):
        if not hasattr(self, 'worker'):
            self.setUpTestData()

    @staticmethod
    def get_expected_data():
        path = "D:\\develop\\Проекты\\python\\django\\drf-test\\backend\\users\\tests\\expected_data.json"
        with open(path) as json_expected_data:
            expected_data = json.loads(json_expected_data.read())
            return expected_data

    def test_read_one_user_data_serializer(self):
        instance = User.objects.filter(id=self.worker.pk)[0]
        serializer = UserSerializer(instance)
        serialized_data = serializer.data
        expected_data = self.get_expected_data()[-1]
        self.assertEqual(serialized_data, expected_data)

    def test_read_all_users_data_serializer(self):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        serialized_data = serializer.data
        expected_data = self.get_expected_data()
        self.assertEqual(expected_data, serialized_data)

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

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.filter(username='customer_225')
        print(user.values())
        print(user[0].customer.discount)
