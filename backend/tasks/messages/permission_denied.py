from enum import StrEnum


class TaskPermissionMessages(StrEnum):
    WORKER_TASKS_ACCESS = 'Not enough worker permission to get this data!'
    CUSTOMER_TASKS_ACCESS = 'Not enough customer permission to get this data!'
    WORKER_TASK_ACCESS = 'Not enough worker permission to do that!'
    CUSTOMER_TASK_ACCESS = 'Not enough customer permission to do that!'
    RUNNING_TASK_ACCESS = 'You cant rewrite processed task!'
