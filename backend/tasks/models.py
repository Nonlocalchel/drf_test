from django.contrib.postgres.indexes import GinIndex, OpClass, HashIndex
from django.db import models
from django.db.models.functions import Upper

from services.mixins.models import SelfValidationMixin

from users.models import Worker, Customer
from tasks.validators import validate_changes, validate_report, check_worker


# Create your models here.
class Task(SelfValidationMixin, models.Model):
    """Task model"""
    validators = [check_worker, validate_report, validate_changes]

    class StatusType(models.TextChoices):
        WAIT = "wait", "Wait"
        IN_PROCESS = "in_process", "In_process"
        DONE = "done", "Done"

    class Meta:
        """Indexes for optimization filter search"""
        indexes = [
            HashIndex(fields=['title'], name='title_hash_index'),
            HashIndex(fields=['status'], name='status_hash_index'),
            GinIndex(OpClass(Upper('title'), name='gin_trgm_ops'),
                     name='title_upper_gin_index'),
        ]

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
