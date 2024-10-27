from users.models import User


def clean_user_input_data(input_validated_data: dict) -> dict:
    user_type = input_validated_data.get('type')
    deleted_key = figure_deleted_data(user_type)
    input_validated_data.pop(deleted_key, None)
    return super().create(input_validated_data)


def figure_deleted_data(user_role: str | None) -> str:
    if user_role == User.UserType.WORKER:
        return User.UserType.CUSTOMER

    return User.UserType.WORKER


def get_auth_users_fields(related_name) -> list[str]:
    basic_user_filds = [field.name for field in User._meta.fields]
    return basic_user_filds + [related_name + '__id']
