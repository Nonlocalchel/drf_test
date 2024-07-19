from django.core.exceptions import ValidationError
from .models import Task

def validate_changes(instance):
    if instance.time_close:
        raise ValidationError(
            {'status': 'Завершенную задачу менять нельзя!'})


def check_worker(instance):
    if not instance.worker:
        if instance.status != Task.StatusType.WAIT:
            raise ValidationError(
                {'worker': 'Задача должна кем-то выполняться!'})


def validate_report(instance):
    report_is_fill = bool(instance.report)

    if instance.status == Task.StatusType.DONE:
        if not report_is_fill:
            raise ValidationError(
                {'report': 'Отчет не может быть пустым'})

        return

    if report_is_fill:
        raise ValidationError(
            {'status': 'Задачу нужно завершить'}
        )