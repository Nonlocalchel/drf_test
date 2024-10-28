from .models import *


def get_auth_users_fields(related_names) -> list[str]:
    basic_user_filds = get_model_fields(User)
    extended_fields = [related_name + '__id' for related_name in related_names]
    return basic_user_filds + extended_fields


def get_user_types() -> list:
    return [user_type.value for user_type in User.UserType]


def get_model_fields(model) -> list:
    return [field.name for field in model._meta.fields]
