from django.test import TestCase

from tasks.models import Task
from tasks.serializers import (
    TaskReadSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskPartialUpdateSerializer
)
from users.models import Worker, Customer


class SerializerTestCase(TestCase):
    """Testing task app serializer"""

    fixtures = [
        'users/tests/fixtures/only_users_backup.json',
        'users/tests/fixtures/customers_data_backup.json', 'users/tests/fixtures/workers_data_backup.json',
        'tasks/tests/fixtures/task_test_backup.json'
    ]

    @classmethod
    def setUpTestData(cls):
        print('\nTask serializer test:')
        cls.worker = Worker.objects.last()
        cls.customer = Customer.objects.last()
        customer = cls.customer
        cls.waiting_task_1 = Task.objects.create(title='Customer test task_1 (wait)', customer=customer)
        cls.waiting_task_2 = Task.objects.create(title='Customer test task_2 (wait)', customer=customer)
        cls.waiting_task_3 = Task.objects.create(title='Customer test task_2 (wait)', customer=customer)

    def setUp(self):
        if not hasattr(self, 'worker'):
            self.setUpTestData()

    def test_read_serializer(self):
        """Get one task data(retrieve)"""
        instance = Task.objects.filter(id=self.waiting_task_1.id)[0]
        serializer = TaskReadSerializer(instance)
        serialized_data = serializer.data
        expected_data = {'id': instance.id, 'title': 'Customer test task_1 (wait)',
                         'time_create': serialized_data['time_create'],
                         'time_update': serialized_data['time_update'],
                         'time_close': None, 'status': 'wait',
                         'report': '', 'customer': 6, 'worker': None}

        self.assertEqual(serialized_data, expected_data)

    def test_create_serializer(self):
        """Create task data"""
        data = {
            "title": "test_task",
            'customer': self.customer.id
        }

        serializer = TaskCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        expected_data = {'title': 'test_task',
                         'time_close': None,
                         'customer': 6,
                         'worker': None}

        self.assertEqual(serializer.data, expected_data)

    def test_update_serializer(self):
        """Update(put) task data"""
        instance = Task.objects.filter(id=self.waiting_task_2.id)[0]
        data = {'title': 'new_title'}
        serializer = TaskUpdateSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serialized_data = serializer.data
        expected_data = {'id': instance.id,
                         'title': 'new_title',
                         'time_create': serialized_data['time_create'],
                         'time_update': serialized_data['time_update'],
                         'time_close': None,
                         'status': 'wait', 'report': '',
                         'customer': 6, 'worker': None}

        self.assertEqual(serialized_data, expected_data)

    def test_partial_update_serializer(self):
        """Partial update(patch) task data"""
        instance = Task.objects.filter(id=self.waiting_task_3.id)[0]
        data = {
            'status': 'in_process',
            'worker': self.worker.id
        }

        serializer = TaskPartialUpdateSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serialized_data = serializer.data
        expected_data = {'id': instance.id,
                         'status': Task.StatusType.IN_PROCESS,
                         'title': 'Customer test task_2 (wait)',
                         'time_create': serialized_data['time_create'],
                         'time_update': serialized_data['time_update'],
                         'time_close': None, 'report': '',
                         'customer': 6, 'worker': 2}

        self.assertEqual(serialized_data, expected_data)
