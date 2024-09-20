import unittest

from rest_framework.test import APITestCase

from tasks.models import Task
from users.models import Worker, Customer


class APITestCaseWithJWT(APITestCase):
    """Тестирование бизнесс-логики приложения"""

    fixtures = ['test_users_backup.json', 'test_customer_backup.json',
                'test_worker_backup.json', 'test_tasks_backup.json']

    @classmethod
    def setUpTestData(cls):
        print('\nCustomer test:')
        cls.worker = Worker.objects.last()
        worker = cls.worker
        cls.customer = Customer.objects.last()
        customer = cls.customer
        cls.waiting_task_1 = Task.objects.create(title='Customer test task_1 (wait)', customer=customer)
        cls.waiting_task_2 = Task.objects.create(title='Customer test task_2 (wait)', customer=customer)
        cls.task_in_process_1 = Task.objects.create(title='Test task_1 (in_process)',
                                                    status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_in_process_2 = Task.objects.create(title='Test task_2 (in_process)',
                                                    status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_done = Task.objects.create(title='Test task_3 (done)',
                                            status=Task.StatusType.IN_PROCESS,
                                            customer=customer, worker=worker)

        cls.task_done.report = 'test'
        cls.task_done.status = Task.StatusType.DONE
        cls.task_done.save()

    def setUp(self):
        pass

    def test_create(self):
        Task.objects.create(title='Customer test task_1 (wait)', customer=self.customer)

    @unittest.expectedFailure
    def test_create_without_customer(self):
        task = Task.objects.create(title='Customer test task_1 (wait)')
        self.assertIsNotNone(task)

    def test_update_run_waiting_task(self):
        Task.objects.filter(id=self.waiting_task_1.id).update(status=Task.StatusType.IN_PROCESS, worker=self.worker)
        self.waiting_task_1.refresh_from_db()
        self.waiting_task_1.save()
        self.assertEqual(self.waiting_task_1.status, Task.StatusType.IN_PROCESS)

    @unittest.expectedFailure
    def test_update_run_waiting_task_without_worker(self):
        Task.objects.filter(id=self.waiting_task_1.id).update(status=Task.StatusType.IN_PROCESS)
        self.waiting_task_1.refresh_from_db()
        self.waiting_task_1.save()

    def test_update_change_wait_or_running_task(self):
        old_title = self.task_in_process_1.title
        Task.objects.filter(id=self.task_in_process_1.id).update(title='new_title')
        self.task_in_process_1.refresh_from_db()
        self.waiting_task_1.save()
        self.assertNotEqual(self.task_in_process_1.title, old_title)
        self.assertEqual(self.task_in_process_1.title, 'new_title')

    @unittest.expectedFailure
    def test_update_report_waiting_or_running_task(self):
        Task.objects.filter(id=self.waiting_task_1.id).update(report='test_report')
        self.waiting_task_1.refresh_from_db()
        self.waiting_task_1.save()

    def test_update_done_running_task(self):
        Task.objects.filter(id=self.task_in_process_1.id).update(status=Task.StatusType.DONE, report='test_report')
        self.task_in_process_1.refresh_from_db()
        self.task_in_process_1.save()
        self.assertEqual(self.task_in_process_1.status, Task.StatusType.DONE)

    @unittest.expectedFailure
    def test_update_done_running_task_without_report(self):
        Task.objects.filter(id=self.task_in_process_1.id).update(status=Task.StatusType.DONE)
        self.task_in_process_1.refresh_from_db()
        self.task_in_process_1.save()
        self.assertEqual(self.task_in_process_1.status, Task.StatusType.DONE)

    @unittest.expectedFailure
    def test_update_done_task(self):
        Task.objects.filter(id=self.done_task.id).update(report='new_title')
        self.task_in_process_1.refresh_from_db()
        self.waiting_task_1.save()