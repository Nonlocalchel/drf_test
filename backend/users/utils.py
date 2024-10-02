from users.models import User


def figure_deleted_data(user_role: str | None) -> str:
    if user_role == User.UserType.WORKER:
        return User.UserType.CUSTOMER

    return User.UserType.WORKER

