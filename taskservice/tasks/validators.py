from django.core.exceptions import ValidationError

from .messages.validation_error import TaskValidationMessages
from .models import Task


def validate_changes(instance):
    if instance.time_close:
        raise ValidationError(
            {'status': TaskValidationMessages.CHANGE_DONE_TASK_ERROR}
        )


def check_worker(instance):
    if not instance.worker:
        if instance.status != Task.StatusType.WAIT:
            raise ValidationError(
                {'worker': TaskValidationMessages.REPORT_FREE_TASK_ERROR}
            )


def validate_report(instance):
    report_is_fill = bool(instance.report)

    if instance.status == Task.StatusType.DONE:
        if not report_is_fill:
            raise ValidationError(
                {'report': TaskValidationMessages.EMPTY_REPORT_ERROR}
            )

        return

    if report_is_fill:
        raise ValidationError(
            {'status': TaskValidationMessages.REPORT_RUNNING_TASK_ERROR}
        )
