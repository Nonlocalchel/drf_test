from users.models import User


def is_super_worker(user: User) -> bool:
    return user.worker.is_super_worker


def is_super_customer(user: User) -> bool:
    return user.customer.is_super_customer


def figure_deleted_data(user_role: str | None) -> str:
    if user_role == User.UserType.WORKER:
        return User.UserType.CUSTOMER

    return User.UserType.WORKER

