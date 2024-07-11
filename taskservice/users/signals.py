from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import *


@receiver(pre_save, sender=User)
def valid_profile_data(sender, instance, **kwargs):
    pass


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

# @receiver(post_save, sender=User)
# def create_company_profile(sender, instance, created, **kwargs):
#     if instance.is_company:
#         if created:
#             Company.objects.create(user=instance)
#     elif instance.is_individual:
#         if created:
#             Individual.objects.create(user=instance)
#     else:
#         pass
#
# @receiver(post_save, sender=User)
# def save_company_profile(sender, instance, **kwargs):
#     if instance.is_company:
#         instance.company_profile.save()
#     elif instance.is_individual:
#         instance.individual_profile.save()
#     else:
#         pass