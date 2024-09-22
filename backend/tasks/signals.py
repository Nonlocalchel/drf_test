from django.db.models.signals import pre_save
from django.dispatch import receiver

from tasks.models import Task


@receiver(pre_save, sender=Task)
def change_status(sender, instance, **kwargs):
    if instance.worker and instance.status == Task.StatusType.WAIT:
        instance.status = Task.StatusType.IN_PROCESS

    if instance.status == Task.StatusType.DONE:
        instance.time_close = instance.time_update
