from django.core.exceptions import ValidationError

from .messages.validation_error import TaskValidationMessages
from .models import Task


def validate_changes(instance):
    if instance.time_close:
        raise ValidationError(
            {'status': TaskValidationMessages.STATUS_DONE_ERROR}
        )


def check_worker(instance):
    if not instance.worker:
        if instance.status != Task.StatusType.WAIT:
            raise ValidationError(
                {'worker': TaskValidationMessages.CHANGE_FREE_TASK_ERROR}
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
            {'status': TaskValidationMessages.UNDONE_TASK_ERROR}
        )


def validate_type_field(user_type, type_data):
    if user_type == 'customer' and type_data:
        raise ValidationError(
            {'customer': TaskValidationMessages.CANT_SET_CUSTOMER_ERROR}
        )
