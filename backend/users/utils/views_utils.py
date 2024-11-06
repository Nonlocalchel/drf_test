import importlib

from django.db.models import QuerySet, Q

from users.models import User, Customer
from users.utils.auth_utils import get_user_types


def filter_user_queryset(user: User, default_queryset: QuerySet) -> QuerySet:
    """Filter user queryset by user type or id"""
    if user.is_staff:
        if user.check_user_type(User.UserType.WORKER):
            return default_queryset

        return User.objects.filter(Q(type=User.UserType.WORKER) | Q(id=user.pk))

    return User.objects.filter(id=user.pk)


def optimize_queryset(queryset: QuerySet) -> QuerySet:
    """Optimize orm fetch by select_related"""
    types = get_user_types()
    return queryset.select_related(*types)


def is_user_account_request(user: User, current_user_id: int) -> bool:
    """Check that it is user gonna to get account"""
    return str(user.pk) == current_user_id


def get_model_by_name(name):
    module = importlib.import_module('users.models')
    cls = getattr(module, name)
    return cls
