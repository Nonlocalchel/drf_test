from users.models import User


def get_user_id(request: any) -> int:
    return request.user.id


def check_user_type(user: User, verifiable_type: str) -> bool:
    return user.type == verifiable_type


def is_super_worker(user: User) -> bool:
    return user.worker.is_super_worker


def is_super_customer(user: User) -> bool:
    return user.customer.is_super_customer
