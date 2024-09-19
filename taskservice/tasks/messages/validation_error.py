from enum import StrEnum


class TaskValidationMessages(StrEnum):
    STATUS_DONE_ERROR = 'Завершенную задачу изменить нельзя!'
    CHANGE_FREE_TASK_ERROR = 'Задача должна кем-то выполняться!'
    EMPTY_REPORT_ERROR = 'Отчет не может быть пустым!'
    UNDONE_TASK_ERROR = 'Задачу нужно завершить!'
    CANT_SET_CUSTOMER_ERROR = 'Нельзя назначать заказчика'

