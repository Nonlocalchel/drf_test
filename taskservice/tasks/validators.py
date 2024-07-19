from django.core.exceptions import ValidationError


def validate_changes(instance):
    if instance.is_done:
        raise ValidationError(
            {'status': 'Завершенную задачу менять нельзя!'})


def check_worker(instance):
    if not instance.worker:
        if instance.status != 'wait':
            raise ValidationError(
                {'worker': 'Задача должна кем-то выполняться!'})


def validate_report(instance):
    if instance.status == 'done':
        if len(instance.report) == 0:
            raise ValidationError(
                {'report': 'Отчет не может быть пустым'})

        return

    if len(instance.report):
        raise ValidationError(
            {'status': 'Задачу нужно завершить'}
        )
