from django.db import models
from ..users.models import Worker, Customer


# Create your models here.

class Task(models.Model):
    class StatusType(models.TextChoices):
        WAIT = "wait", "Wait"
        IN_PROCESS = "worker", "Worker"
        DONE = "done", "Done"

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    time_close = models.DateTimeField(auto_now=True, verbose_name="Время закрытия")
    status = models.CharField(max_length=50,
                              choices=StatusType,
                              default=StatusType.WAIT,
                              )
    report = models.TextField(blank=True, verbose_name="Отчет")
    consumer = models.OneToOneField(Worker, on_delete=models.CASCADE,
                                    related_name='task', verbose_name="Заказчик")
    worker = models.OneToOneField(Worker, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='task', verbose_name="Исполнитель")
