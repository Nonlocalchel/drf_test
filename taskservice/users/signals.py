from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import *


# @receiver(pre_save, sender=User)
# def change_user_data(sender, instance,create **kwargs):
#     if created:
#         instance.set_password(instance.password)


@receiver(post_save, sender=User)
def create_special_profile(sender, instance, created, **kwargs):
    if created:
        if instance.type == 'customer':
            Customer.objects.create(user=instance)
        elif instance.type == 'worker':
            Worker.objects.create(user=instance)
    else:
        pass


@receiver(post_save, sender=User)
def save_special_profile(sender, instance, created, **kwargs):
    if created:
        if instance.type == 'customer':
            instance.customer.save()
        elif instance.type == 'worker':
            instance.worker.save()
    else:
        pass
