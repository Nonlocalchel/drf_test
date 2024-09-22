from enum import StrEnum


class UserPermissionMessages(StrEnum):
    WORKER_ACCESS = 'You are not a worker!'
    CUSTOMER_ACCESS = 'You are not a customer!'
    SUPER_WORKER_ACCESS = 'You are not a worker with extra permissions!'
    SUPER_CUSTOMER_ACCESS = 'You are not a customer with extra permissions!'
