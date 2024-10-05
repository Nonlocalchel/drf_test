from django.db.models import Q

from tasks.models import Task
from users.models import User


def figure_deleted_data(user_role: str | None) -> str:
    if user_role == User.UserType.WORKER:
        return User.UserType.CUSTOMER

    return User.UserType.WORKER


def filter_user_queryset(user: User, default_queryset: Task) -> Task:
    if user.check_user_type(User.UserType.WORKER):
        if user.is_staff:
            return default_queryset

        worker_id = user.worker.id
        queryset = default_queryset.filter(Q(worker=worker_id) | Q(worker__isnull=True))

    if user.check_user_type(User.UserType.CUSTOMER):
        queryset = default_queryset.filter(customer=user.customer.id)

    return queryset
