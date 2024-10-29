import copy

from django.db.models import QuerySet

from users.models import User



def fix_serializer_fields(instance, fields: dict, data: dict | None = None) -> dict:
    """Dynamic change nested fields of UserSerializer"""
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
    """Format representation of user data"""
    repr_copy = copy.deepcopy(representation)
    user_types = get_user_types()
    for user_type in user_types:
        repr_copy.pop(user_type, None)

    repr_copy['profile_data'] = representation[current_user_type]
    return repr_copy


def get_instance_type(instance):
    """Get instance in to_representation method"""
    return instance.type if not isinstance(instance, dict) else instance.get('type')
