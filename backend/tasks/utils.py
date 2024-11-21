from django.db.models import Q, QuerySet
from django.http import QueryDict

from tasks.models import Task
from users.models import User


def filter_task_queryset(user: User, default_queryset: QuerySet) -> QuerySet:
    """Filter task queryset by user type or id"""
    if user.check_user_type(User.UserType.WORKER):
        if user.is_staff:
            return default_queryset

        worker_id = user.worker.id
        return default_queryset.filter(Q(worker=worker_id) | Q(worker__isnull=True))

    if user.check_user_type(User.UserType.CUSTOMER):
        return default_queryset.filter(customer=user.customer.id)


def set_task_customer(task: dict, user: User) -> None:
    """Set task a customer"""
    if user.check_user_type('customer'):
        task['customer'] = user.customer.id


def take_task_in_process(task: dict, user: User) -> None:
    """Take task in process"""
    # if isinstance(task, QueryDict):
    #     task = task.pop()

    task['worker'] = user.worker.id


def done_task(task: dict) -> None:
    """Done task"""
    task['status'] = Task.StatusType.DONE
