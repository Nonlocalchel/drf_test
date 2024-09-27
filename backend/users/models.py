from django.contrib.auth.models import AbstractUser
from django.db import models

from services.mixins.models import SelfValidationMixin, FieldTrackerMixin, GetFieldRelatedNameMixin
from users.validators import validate_change_user_type, validate_add_worker_data_to_user, validate_worker_photo


# Create your models here.
class User(SelfValidationMixin, FieldTrackerMixin, AbstractUser):
    validators = [validate_change_user_type, validate_worker_photo]

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


class Worker(SelfValidationMixin, GetFieldRelatedNameMixin, models.Model):
    validators = [validate_add_worker_data_to_user]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker')
    exp = models.IntegerField(blank=True, null=True)
    is_super_worker = models.BooleanField(default=False)


class Customer(SelfValidationMixin, GetFieldRelatedNameMixin, models.Model):
    validators = [validate_add_worker_data_to_user]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    discount = models.IntegerField(blank=True, null=True)
    is_super_customer = models.BooleanField(default=False)
