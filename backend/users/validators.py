from django.core.exceptions import ValidationError


def validate_change_user_type(instance):
    if instance.has_changed('type'):
        raise ValidationError(
            {'type': f'Пользователь {instance.username} уже имеет тип!'}
        )


def validate_worker_photo(instance):
    if instance.type == 'worker':
        if not bool(instance.photo):
            raise ValidationError(
                {'photo': f'Пользователь {instance.username} является работником и должен иметь фото!'}
            )


def validate_add_worker_data_to_user(instance):
    if hasattr(instance, 'user'):
        user = instance.user
        related_model_field_name = instance.get_related_field_name('user')
        if user.type != related_model_field_name:
            raise ValidationError(
                {
                    related_model_field_name: f'Пользователь {user.username} является {user.type} и вы не можете назначить ему тип {related_model_field_name}!'}
            )
