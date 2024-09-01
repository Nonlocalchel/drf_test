from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import *


@receiver(pre_save, sender=User)
def create_special_profile(sender, instance, **kwargs):
    user_password = instance.password
    if user_password.startswith('pbkdf2_sha256'):
        return

    instance.set_password(user_password)


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
