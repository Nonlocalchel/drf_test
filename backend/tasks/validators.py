from django.core.exceptions import ValidationError

from .messages.validation_error import TaskValidationMessages


def validate_changes(instance):
    """Check that changed task isn't done"""
    if instance.time_close:
        raise ValidationError(
            {'status': TaskValidationMessages.CHANGE_DONE_TASK_ERROR}
        )


def check_worker(instance):
    """Does not allow an employee to intercept someone else's task"""
    if instance.status != 'wait':
        if not instance.worker_id:
            raise ValidationError(
                {'worker': TaskValidationMessages.REPORT_FREE_TASK_ERROR}
            )


def validate_report(instance):
    """Validate report depending on status"""
    report_is_fill = bool(instance.report)

    if instance.status == 'done':
        if not report_is_fill:
            raise ValidationError(
                {'report': TaskValidationMessages.EMPTY_REPORT_ERROR}
            )

        return

    if report_is_fill:
        raise ValidationError(
            {'status': TaskValidationMessages.REPORT_RUNNING_TASK_ERROR}
        )
