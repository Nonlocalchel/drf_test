from django.db import utils
from django.test import TestCase
from django.core.exceptions import ValidationError

from tasks.messages.validation_error import TaskValidationMessages
from tasks.models import Task
from users.models import Worker, Customer


class BusinessTestCase(TestCase):
    """Тестирование бизнесс-логики приложения"""

    fixtures = ['test_users_backup.json', 'test_customer_backup.json',
                'test_worker_backup.json', 'test_tasks_backup.json']

    @classmethod
    def setUpTestData(cls):
        print('\nBusiness test:')
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

        cls.task_in_process_3 = Task.objects.create(title='Test task_3 (in_process)',
                                                    status=Task.StatusType.IN_PROCESS,
                                                    customer=customer, worker=worker)

        cls.task_done = Task.objects.create(title='Test task_3 (done)',
                                            status=Task.StatusType.IN_PROCESS,
                                            customer=customer, worker=worker)

        cls.task_done.report = 'test'
        cls.task_done.status = Task.StatusType.DONE
        cls.task_done.save()

    def setUp(self):
        if not hasattr(self, 'worker'):
            self.setUpTestData()

    def test_create(self):
        Task.objects.create(title='Customer test task_1 (wait)', customer=self.customer)

    def test_create_without_customer(self):
        self.assertRaisesRegex(
            utils.IntegrityError,
            r'NOT NULL constraint failed',
            Task.objects.create,
            title='Customer test task_1 (wait)'
        )

    def test_update_run_waiting_task(self):
        Task.objects.filter(id=self.waiting_task_1.id).update(worker=self.worker)
        self.waiting_task_1.refresh_from_db()
        self.waiting_task_1.save()
        self.assertEqual(self.waiting_task_1.status, Task.StatusType.IN_PROCESS)

    def test_update_run_waiting_task_without_worker(self):
        Task.objects.filter(id=self.waiting_task_2.id).update(status=Task.StatusType.IN_PROCESS)
        self.waiting_task_2.refresh_from_db()
        self.assertRaisesRegex(
            ValidationError,
            TaskValidationMessages.REPORT_FREE_TASK_ERROR,
            self.waiting_task_2.save
        )

    def test_update_change_wait_or_running_task(self):
        Task.objects.filter(id=self.task_in_process_2.id).update(title='new_title')
        self.task_in_process_2.refresh_from_db()
        self.waiting_task_2.save()
        self.assertEqual(self.task_in_process_2.title, 'new_title')

    # @unittest.expectedFailure
    def test_update_report_waiting_or_running_task(self):
        Task.objects.filter(id=self.waiting_task_2.id).update(report='test_report')
        self.waiting_task_2.refresh_from_db()
        self.assertRaisesRegex(
            ValidationError,
            TaskValidationMessages.REPORT_RUNNING_TASK_ERROR,
            self.waiting_task_2.save
        )

    def test_update_done_running_task(self):
        Task.objects.filter(id=self.task_in_process_3.id).update(status=Task.StatusType.DONE, report='test_report')
        self.task_in_process_3.refresh_from_db()
        self.task_in_process_3.save()
        self.assertEqual(self.task_in_process_3.status, Task.StatusType.DONE)
        self.assertIsNotNone(self.task_in_process_3.time_close)

    def test_update_done_running_task_without_report(self):
        Task.objects.filter(id=self.task_in_process_2.id).update(status=Task.StatusType.DONE)
        self.task_in_process_2.refresh_from_db()
        self.assertRaisesRegex(
            ValidationError,
            TaskValidationMessages.EMPTY_REPORT_ERROR,
            self.task_in_process_2.save
        )

    def test_update_done_task(self):
        Task.objects.filter(id=self.task_done.id).update(report='new_report')
        self.task_done.refresh_from_db()
        self.assertRaisesRegex(
            ValidationError,
            TaskValidationMessages.CHANGE_DONE_TASK_ERROR,
            self.task_done.save
        )
