from django.core.exceptions import ValidationError
from django.db import models

from users.models import Worker, Customer
from .validators import *


# Create your models here.

class Task(models.Model):
    class StatusType(models.TextChoices):
        WAIT = "wait", "Wait"
        IN_PROCESS = "worker", "Worker"
        DONE = "done", "Done"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    time_close = models.DateTimeField(blank=True, null=True, editable=False, verbose_name="Время изменения")
    status = models.CharField(max_length=50, choices=StatusType, default=StatusType.WAIT)
    report = models.TextField(blank=True, verbose_name="Отчет")
    is_done = models.BooleanField(default=False, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='task', verbose_name="Заказчик")
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='task', verbose_name="Исполнитель")

    def __str__(self):
        return self.title

    def get_time_close(self):
        return self.time_update if self.status == 'done' else None

    def clean(self):
        validate_changes(self)
        check_worker(self)
        validate_report(self)


