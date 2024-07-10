from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=User)
def create_company_profile(sender, instance, created, **kwargs):
    print(kwargs)
    print(f"{type(instance)} is created!")


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