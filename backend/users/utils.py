from services.model_utils import *
from .models import *


def figure_deleted_data(user_role: str | None) -> str:
    if user_role == User.UserType.WORKER:
        return User.UserType.CUSTOMER

    return User.UserType.WORKER


def get_auth_users_fields(related_names) -> list[str]:
    basic_user_filds = get_model_fields(User)
    extended_fields = [related_name + '__id' for related_name in related_names]
    return basic_user_filds + extended_fields


def format_data_dict(data_dict: dict) -> None:
    added_user_type = data_dict['type']
    user_types = get_user_types()
    user_types.remove(added_user_type)
    for user_type in user_types:
        data_dict.pop(user_type, None)

    user_profile_data_class = get_class_by_name(added_user_type, module_name=__name__)
    user_profile_data = get_dict_instance(user_profile_data_class)
    data_dict[added_user_type] = user_profile_data


def get_user_types() -> list:
    return [user_type.value for user_type in User.UserType]



