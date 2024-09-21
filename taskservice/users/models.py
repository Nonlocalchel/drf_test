from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from services.extended_models.ModelWithOriginal import ModelWithOriginal
from services.extended_models.ModelWithSelfCleaning import ModelWithSelfCleaning


# Create your models here.
class User(AbstractUser, ModelWithOriginal, ModelWithSelfCleaning):
    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        WORKER = "worker", "Worker"

    phone = models.CharField(max_length=50, unique=True, null=True, verbose_name="Номер телефона")
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    type = models.CharField(max_length=50, choices=UserType, default=UserType.CUSTOMER)

    def check_user_type(self, verifiable_type: str) -> bool:
        return self.type == verifiable_type

    def clean(self):
        if 'type' in self.changed_fields and not self.pk is None:
            raise ValidationError(
                {'type': f'Пользователь уже имеет тип!'}
            )

        return super().clean()


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='worker')
    exp = models.IntegerField(blank=True, null=True)
    is_super_worker = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer')
    discount = models.IntegerField(blank=True, null=True)
    is_super_customer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
