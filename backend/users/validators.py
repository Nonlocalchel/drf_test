from django.core.exceptions import ValidationError


def validate_change_user_type(instance):
    if instance.has_changed('type'):
        raise ValidationError(
            {'type': f'Пользователь {instance.username} уже имеет тип!'}
        )


def validate_add_user_role_data(instance):
    if hasattr(instance.customer, 'pk') and hasattr(instance.worker, 'pk'):
        raise ValidationError(
            {'type': f'Пользователь {instance.username} является {instance.type}!'}
        )


def validate_worker_photo(instance):
    if instance.type == 'worker':
        if instance.photo is None:
            raise ValidationError(
                {'photo': f'Пользователь {instance.username} является работником и должен иметь фото!'}
            )
