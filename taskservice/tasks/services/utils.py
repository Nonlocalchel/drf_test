from django.db.models import Q, QuerySet


def get_safe_methods(methods: list[str]) -> list[str]:
    return [method.lower() for method in methods]


def get_job_query(default_queryset: QuerySet, query_type: str, user_id: int) -> QuerySet:
    worker_task = Q(worker=user_id)
    free_tasks = Q(worker__isnull=True)
    filter_params = worker_task | free_tasks

    if query_type == 'free':
        filter_params = free_tasks

    if query_type == 'main':
        filter_params = worker_task

    return default_queryset.filter(filter_params)
