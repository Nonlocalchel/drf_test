from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import *


@receiver(pre_save, sender=User)
def create_special_profile(sender, instance, **kwargs):
    """Шифрование пароля при его изменении"""
    user_password = instance.password
    if user_password.startswith('pbkdf2_sha256'):
        return

    instance.set_password(user_password)

#перенести жто в userManager
@receiver(post_save, sender=User)
def create_special_profile(sender, instance, created, **kwargs):
    if created:
        if instance.type == 'customer':
            customer = Customer.objects.create(user=instance)
            customer.save()
        elif instance.type == 'worker':
            worker = Worker.objects.create(user=instance)
            worker.save()
    else:
        pass


# @receiver(post_save, sender=User)
# def save_special_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.type == 'customer':
#             instance.customer.save()
#         elif instance.type == 'worker':
#             instance.worker.save()
#     else:
#         pass
