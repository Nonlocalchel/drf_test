from itertools import chain

from django.db.models import Q


def get_safe_methods(methods):
    return [method.lower() for method in methods]


def get_user_id(request):
    return request.user.id


def get_right_query(queryset, case):
    empty_query = queryset.none()
    return queryset if not case else empty_query

#
# queryset_1 = get_right_query(queryset.filter(worker=user_id), query_type == 'free')
# queryset_2 = get_right_query(queryset.filter(worker=None), query_type == 'main')
#
# return queryset_1 | queryset_2
def get_job_query(default_queryset, query_type, user_id):
    worker_task = Q(worker=user_id)
    free_tasks = Q(worker__isnull=True)
    filter_params = worker_task | free_tasks

    if query_type == 'free':
        filter_params = free_tasks

    if query_type == 'main':
        filter_params = worker_task


    return default_queryset.filter(filter_params)



def check_user_type(user, verifiable_type):
    return user.type == verifiable_type
