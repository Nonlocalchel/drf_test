from users.models import User


def is_super_worker(user: User) -> bool:
    return user.worker.is_super_worker


def is_super_customer(user: User) -> bool:
    return user.customer.is_super_customer
