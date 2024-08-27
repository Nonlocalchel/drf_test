from itertools import chain


def get_safe_methods(methods):
    return [method.lower() for method in methods]


def get_user_id(request):
    return request.user.id


def get_right_query(queryset, case):
    empty_query = queryset.none()
    return queryset if not case else empty_query


def check_user_type(user, verifiable_type):
    return user.type == verifiable_type
