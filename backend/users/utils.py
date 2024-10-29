import copy

from django.db.models import QuerySet
from rest_framework import serializers

from .models import *


def get_auth_users_fields(related_names) -> list[str]:
    basic_user_filds = get_model_fields(User)
    extended_fields = [related_name + '__id' for related_name in related_names]
    return basic_user_filds + extended_fields


def get_user_types() -> list:
    return [user_type.value for user_type in User.UserType]


def get_model_fields(model) -> list:
    return [field.name for field in model._meta.fields]


def fix_serializer_fields(instance, fields: dict, data: dict | None = None) -> dict:
    fixed_fields = fields.copy()

    if not isinstance(instance, QuerySet):
        user_types = get_user_types()
        if not instance:
            current_user_type = data.get('type', User.UserType.CUSTOMER)
        else:
            current_user_type = instance.type

        for user_type in user_types:
            if current_user_type == user_type:
                continue

            fixed_fields.pop(user_type)

    return fixed_fields


def format_repr(representation: dict, current_user_type: str) -> dict:
    repr_copy = copy.deepcopy(representation)
    user_types = get_user_types()
    for user_type in user_types:
        repr_copy.pop(user_type, None)

    repr_copy['profile_data'] = representation[current_user_type]
    return repr_copy



