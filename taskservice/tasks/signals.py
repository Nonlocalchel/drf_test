from django.db.models import signals
from django.dispatch import receiver

from tasks.models import Task


@receiver(signals.pre_save, sender=Task)
def change_status(sender, instance, **kwargs):
    if instance.worker and instance.status == Task.StatusType.WAIT:
        instance.status = Task.StatusType.IN_PROCESS
        return

    if instance.status == Task.StatusType.DONE:
        instance.time_close = instance.time_update
        instance.is_done = True


# @receiver(signals.post_save, sender=Task)
# def create_special_profile(sender, instance, created, **kwargs):
#     if not (instance.status == 'done' and not instance.is_done):
#         return
#
#     instance.time_close = instance.time_update
#     instance.is_done = True
#     instance.save()


# @receiver(signals.post_save, sender=Task)
# def create_special_profile(sender, instance, created, **kwargs):
#     if not (instance.worker and instance.status == 'wait'):
#         return
#
#     instance.status = 'worker'
#
#
#     instance.save()
