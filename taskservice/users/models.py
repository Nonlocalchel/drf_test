from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=50, unique=True, null=True, verbose_name="Номер телефона")
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"


# class Worker(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='worker_profile')
#     exp = models.IntegerField(null=True)
#
#
#     is_super_worker = models.BooleanField(default=False)
#     #override save()?
#
#
# class Consumer(models.Model):
#     discount = models.IntegerField(null=True)
#     is_super_consumer = models.BooleanField(default=False)


