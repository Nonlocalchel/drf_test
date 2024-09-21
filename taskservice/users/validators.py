from django.core.exceptions import ValidationError


def validate_change_user_type(instance):
    if 'type' in instance.changed_fields and not instance.pk is None:
        raise ValidationError(
            {'type': f'Пользователь {instance.username} уже имеет тип!'}
        )