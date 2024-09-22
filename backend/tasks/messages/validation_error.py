from enum import StrEnum


class TaskValidationMessages(StrEnum):
    CHANGE_DONE_TASK_ERROR = 'Завершенную задачу изменить нельзя!'
    REPORT_FREE_TASK_ERROR = 'Задача должна кем-то выполняться!'
    EMPTY_REPORT_ERROR = 'Отчет не может быть пустым!'
    REPORT_RUNNING_TASK_ERROR = 'Задачу нужно завершить!'
    CANT_SET_CUSTOMER_ERROR = 'Нельзя назначать заказчика'

