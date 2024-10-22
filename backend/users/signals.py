from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import *


@receiver(pre_save, sender=User)
def create_profile(sender, instance, **kwargs):
    """Шифрование пароля при его изменении"""
    user_password = instance.password
    if user_password.startswith('pbkdf2_sha256'):
        return

    instance.set_password(user_password)
