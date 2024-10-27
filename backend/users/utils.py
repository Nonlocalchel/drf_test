from users.models import User


def clean_user_input_data(input_validated_data: dict) -> dict:
    user_type = input_validated_data.get('type')
    deleted_key = figure_deleted_data(user_type)
    input_validated_data.pop(deleted_key, None)
    return input_validated_data


def figure_deleted_data(user_role: str | None) -> str:
    if user_role == User.UserType.WORKER:
        return User.UserType.CUSTOMER

    return User.UserType.WORKER


def get_auth_users_fields(related_names) -> list[str]:
    basic_user_filds = [field.name for field in User._meta.fields]
    extended_fields = [related_name + '__id' for related_name in related_names]
    return basic_user_filds + extended_fields


def get_user_types() -> list:
    return [user_type.value for user_type in User.UserType]
