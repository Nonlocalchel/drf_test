from tasks.models import Task

def validate_changes(instance):
    if instance.time_close:
        return {'status': 'Завершенную задачу изменить нельзя!'}


def check_worker(instance):
    if not instance.worker:
        if instance.status != Task.StatusType.WAIT:
            return {'worker': 'Задача должна кем-то выполняться!'}


def validate_report(instance):
    report_is_fill = bool(instance.report)

    if instance.status == Task.StatusType.DONE:
        if not report_is_fill:
            return {'report': 'Отчет не может быть пустым'}

        return

    if report_is_fill:
        return {'status': 'Задачу нужно завершить'}
