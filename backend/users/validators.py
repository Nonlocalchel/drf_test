from django.core.exceptions import ValidationError


def validate_change_user_type(instance):
    if instance.has_changed('type'):
        raise ValidationError(
            {'type': f'Пользователь {instance.username} уже имеет тип!'}
        )


# def validate_add_user_role_data(instance):
#     if hasattr(instance, 'customer') and hasattr(instance, 'worker'):
#         raise ValidationError(
#             {'type': f'Пользователь {instance.username} является {instance.type}!'}
#         )


def validate_worker_photo(instance):
    if instance.type == 'worker':
        if not bool(instance.photo):
            raise ValidationError(
                {'photo': f'Пользователь {instance.username} является работником и должен иметь фото!'}
            )


def validate_add_worker_data_to_user(instance):
    if hasattr(instance, 'user'):
        user = instance.user
        model_related_field_name = instance.get_field_related_name('user')
        if user.type != model_related_field_name:
            raise ValidationError(
                {
                    model_related_field_name: f'Пользователь {user.username} является {user.type} и вы не можете назначить ему тип {model_related_field_name}!'}
            )
