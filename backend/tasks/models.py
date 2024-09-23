from django.db import models

from services.mixins.models import SelfCleaningAndValidationMixin

from users.models import Worker, Customer
from tasks.validators import validate_changes, validate_report, check_worker


# Create your models here.
class Task(SelfCleaningAndValidationMixin, models.Model):
    validators = [check_worker, validate_report, validate_changes]

    class StatusType(models.TextChoices):
        WAIT = "wait", "Wait"
        IN_PROCESS = "in_process", "In_process"
        DONE = "done", "Done"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    time_close = models.DateTimeField(blank=True, null=True, editable=False, verbose_name="Время закрытия")
    status = models.CharField(max_length=50, choices=StatusType, default=StatusType.WAIT)
    report = models.TextField(blank=True, verbose_name="Отчет")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='task', verbose_name="Заказчик")
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='task', verbose_name="Исполнитель")

    def __str__(self):
        return self.title
