from users.models import User


def get_auth_users_fields(related_names) -> list[str]:
    """Construct needed fields in auth request for optimization"""
    basic_user_filds = [field.name for field in User.get_model_fields()]
    extended_fields = [related_name + '__id' for related_name in related_names]
    return basic_user_filds + extended_fields


def get_user_types() -> list:
    """Get user types on User.UserType Enum"""
    return [user_type.value for user_type in User.UserType]

