from django.db.models import QuerySet

from users.models import User


def filter_user_queryset(user: User, default_queryset: QuerySet) -> QuerySet:
    if user.is_staff:
        if user.check_user_type(User.UserType.WORKER):
            return default_queryset

    return User.objects.none()