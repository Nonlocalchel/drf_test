from django.db.models import Q, QuerySet
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request


def get_safe_methods() -> list[str]:
    return [method.lower() for method in SAFE_METHODS]


def get_customer_queryset(default_queryset: QuerySet, user_id: int):
    """При проблемах с оптимизациецй можно возвращать только параметры фильтрации"""

    customer_task = Q(customer=user_id)
    filter_params = customer_task
    return default_queryset.filter(filter_params)


def get_worker_queryset(default_queryset: QuerySet, user_id: int) -> QuerySet:
    """При проблемах с оптимизациецй можно возвращать только параметры фильтрации"""

    worker_task = Q(worker=user_id)
    free_tasks = Q(worker__isnull=True)
    filter_params = worker_task | free_tasks
    return default_queryset.filter(filter_params)
