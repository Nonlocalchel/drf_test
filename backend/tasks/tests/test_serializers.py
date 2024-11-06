from django.test import TestCase

from services.ImageWorker import ImageCreator
from tasks.models import Task
from tasks.serializers import (
    TaskReadSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskPartialUpdateSerializer
)
from users.models import User


class SerializerTestCase(TestCase):
    """Testing task app serializer"""
    image_creator = ImageCreator

    @classmethod
    def setUpTestData(cls):
        print('\nTask serializer test:')
        cls.user_customer = User.objects.create(password='customer_super_ps_387',
                                                username='task_serializer_test_customer_1')
        cls.user_worker = User.objects.create(password='worker_super_ps_387',
                                              username='task_serializer_test_worker_1',
                                              type=User.UserType.WORKER, photo=cls.image_creator.get_fake_image())

        customer = cls.user_customer.customer
        cls.waiting_task_1 = Task.objects.create(title='Customer test task_1 (wait)', customer=customer)
        cls.waiting_task_2 = Task.objects.create(title='Customer test task_2 (wait)', customer=customer)
        cls.waiting_task_3 = Task.objects.create(title='Customer test task_2 (wait)', customer=customer)

    def setUp(self):
        pass

    def test_read_serializer(self):
        """Get one task data(retrieve)"""
        instance = Task.objects.filter(id=self.waiting_task_1.id)[0]
        serializer = TaskReadSerializer(instance)
        serialized_data = serializer.data
        expected_data = {'id': instance.id, 'title': 'Customer test task_1 (wait)',
                         'time_create': serialized_data['time_create'],
                         'time_update': serialized_data['time_update'],
                         'time_close': None, 'status': 'wait',
                         'report': '', 'customer': self.user_customer.customer.id,
                         'worker': None}

        self.assertEqual(serialized_data, expected_data)

    def test_create_serializer(self):
        """Create task data"""
        data = {
            "title": "test_task",
            'customer': self.user_customer.customer.id
        }

        serializer = TaskCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        expected_data = {'title': 'test_task',
                         'time_close': None,
                         'customer': data['customer'],
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
                         'customer': self.user_customer.customer.id,
                         'worker': None}

        self.assertEqual(serialized_data, expected_data)

    def test_partial_update_serializer(self):
        """Partial update(patch) task data"""
        instance = Task.objects.filter(id=self.waiting_task_3.id)[0]
        data = {
            'status': 'in_process',
            'worker': self.user_worker.worker.id
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
                         'customer': self.user_customer.customer.id,
                         'worker': data['worker']}

        self.assertEqual(serialized_data, expected_data)
