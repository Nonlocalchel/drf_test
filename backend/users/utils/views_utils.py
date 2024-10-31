from django.db.models import QuerySet

from users.models import User
from users.utils.auth_utils import get_user_types


def filter_user_queryset(user: User, default_queryset: QuerySet) -> QuerySet:
    if user.is_staff:
        if user.check_user_type(User.UserType.WORKER):
            return default_queryset

        return User.objects.filter(type=User.UserType.WORKER)

    return User.objects.filter(id=user.pk)


def optimize_queryset(queryset):
    types = get_user_types()
    return queryset.select_related(*types)


def is_user_account_request(user, current_user_id):
    return str(user.id) == current_user_id
