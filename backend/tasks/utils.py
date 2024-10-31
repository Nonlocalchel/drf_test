from django.db.models import Q, QuerySet

from tasks.models import Task
from users.models import User


def filter_task_queryset(user: User, default_queryset: QuerySet) -> QuerySet:
    if user.check_user_type(User.UserType.WORKER):
        if user.is_staff:
            return default_queryset

        worker_id = user.worker.id
        queryset = default_queryset.filter(Q(worker=worker_id) | Q(worker__isnull=True))

    if user.check_user_type(User.UserType.CUSTOMER):
        queryset = default_queryset.filter(customer=user.customer.id)

    return queryset


def take_task_in_process(task, user):
    task['worker'] = user.worker.id


def done_task(task):
    task['status'] = Task.StatusType.DONE
