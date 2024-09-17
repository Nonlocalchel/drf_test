from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models

from services.ModelWithOriginal import ModelWithOriginal
from services.SelfCleaningModel import SelfCleaningModel


# Create your models here.

class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, password, **extra_fields)
        """
        user=super().create_user(username, email, password, **extra_fields)
        if user.type == 'customer':
            customer = Customer.objects.create(user=user)
            customer.save()
        elif user.type == 'worker':
            worker = Worker.objects.create(user=user)
            worker.save()
            
        return user
        """


class User(AbstractUser, ModelWithOriginal, SelfCleaningModel):
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

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    objects = CustomUserManager()


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
