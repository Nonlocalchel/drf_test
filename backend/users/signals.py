from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import *
from .tasks import create_profile_data
from .utils.views_utils import get_model_by_name


@receiver(pre_save, sender=User)
def create_profile(sender, instance, **kwargs):
    """Encrypting a password when creating or changing it"""
    user_password = instance.password
    if user_password.startswith('pbkdf2_sha256'):
        return

    instance.set_password(user_password)


@receiver(post_save, sender=User)
def create_special_profile(sender, instance, created, **kwargs):
    """Create professional data after save user"""
    if not created:
        return

    create_profile_data(instance.id)
    # user_type = instance.type

    # create_profile_data.delay(instance.pk, user_type)
    # class_name = user_type.capitalize()
    # profile_data_model = get_model_by_name(class_name)
    # profile_data = profile_data_model(user=instance)
    # profile_data.save()
