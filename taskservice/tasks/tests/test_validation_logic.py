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
        worker = Worker.objects.last()
        customer = Customer.objects.last()
        cls.task = Task.objects.create(title='Customer test task_1 (wait)', customer=customer)
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
        pass

    def test_create_without_customer(self):
        pass

    def test_update_done_task(self):
        pass

    def test_update_change_worker(self):
        pass

    def test_update_report_running_task(self):
        pass

    def test_update_report_waiting_task(self):
        pass