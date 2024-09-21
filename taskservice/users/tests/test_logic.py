# from django.test import TestCase
#
# # Create your tests here.
#
# from django.core.exceptions import ValidationError
#
# from tasks.messages.validation_error import TaskValidationMessages
# from tasks.models import Task
# from users.models import Worker, Customer
#
#
# class BusinessTestCase(TestCase):
#     """Тестирование бизнесс-логики приложения"""
#
#     @classmethod
#     def setUpTestData(cls):
#         print('\nBusiness test:')
#         cls.worker = Worker.objects.last()
#         worker = cls.worker
#         cls.customer = Customer.objects.last()
#         customer = cls.customer
#         cls.waiting_task_1 = Task.objects.create(title='Customer test task_1 (wait)', customer=customer)
#         cls.waiting_task_2 = Task.objects.create(title='Customer test task_2 (wait)', customer=customer)
#         cls.task_in_process_1 = Task.objects.create(title='Test task_1 (in_process)',
#                                                     status=Task.StatusType.IN_PROCESS,
#                                                     customer=customer, worker=worker)
#
#         cls.task_in_process_2 = Task.objects.create(title='Test task_2 (in_process)',
#                                                     status=Task.StatusType.IN_PROCESS,
#                                                     customer=customer, worker=worker)
#
#         cls.task_in_process_3 = Task.objects.create(title='Test task_3 (in_process)',
#                                                     status=Task.StatusType.IN_PROCESS,
#                                                     customer=customer, worker=worker)
#
#         cls.task_done = Task.objects.create(title='Test task_3 (done)',
#                                             status=Task.StatusType.IN_PROCESS,
#                                             customer=customer, worker=worker)
#
#         cls.task_done.report = 'test'
#         cls.task_done.status = Task.StatusType.DONE
#         cls.task_done.save()

