from rest_framework.permissions import SAFE_METHODS


def get_safe_methods() -> list[str]:
    return [method.lower() for method in SAFE_METHODS]