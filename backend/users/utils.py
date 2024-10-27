from users.models import User


def figure_deleted_data(user_role: str | None) -> str:
    if user_role == User.UserType.WORKER:
        return User.UserType.CUSTOMER

    return User.UserType.WORKER


def get_all_user_types() -> list[str]:
    return [user_type.value for user_type in User.UserType]


def get_auth_users_fields(related_names) -> list[str]:
    basic_user_filds = [field.name for field in User._meta.fields]
    related_fields = [related_name+'__id' for related_name in related_names]
    return basic_user_filds + related_fields
