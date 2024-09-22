from django.core.exceptions import ValidationError


def validate_change_user_type(instance):
    if 'type' in instance.changed_fields and not instance.pk is None:
        raise ValidationError(
            {'type': f'Пользователь {instance.username} уже имеет тип!'}
        )


def validate_worker_photo(instance):
    if instance.type == 'worker':
        if instance.photo is None:
            raise ValidationError(
                {'photo': f'Пользователь {instance.username} является работником и должен иметь фото!'}
            )