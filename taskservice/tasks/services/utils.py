def get_safe_methods(methods):
    return [method.lower() for method in methods]


def get_user_id(request):
    return request.user.id
