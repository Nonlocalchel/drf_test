from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models

from services.mixins.models import SelfValidationMixin, FieldTrackerMixin, GetFieldRelatedNameMixin
from users.validators import (
    validate_change_user_type,
    validate_add_worker_data_to_user,
    validate_worker_photo
)


class ExtendedManager(UserManager):
    def get_queryset(self, all=None):  # , all=None
        types = [user_type.value for user_type in User.UserType]
        fields = [(field.name) for field in User._meta.fields] + ['worker__id', 'customer__id']
        return super().get_queryset().select_related(*types)  # .only(*fields)


# Create your models here.
class User(SelfValidationMixin, FieldTrackerMixin, AbstractUser):
    validators = [validate_change_user_type, validate_worker_photo]

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        WORKER = "worker", "Worker"

    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    type = models.CharField(max_length=50, choices=UserType, default=UserType.CUSTOMER)
    phone = models.CharField(max_length=50, validators=[
        RegexValidator(
            regex=r'^(\+)?((\d{2,3}) ?\d|\d)(([ -]?\d)|( ?(\d{2,3}) ?)){5,12}\d$',
            message="Enter a valid registration number in the format ABC123.",
            code="invalid_registration",
        ),
    ],
                             unique=True,
                             null=True,
                             verbose_name="Номер телефона"
                             )

    def check_user_type(self, verifiable_type: str) -> bool:
        return self.type == verifiable_type

    # objects = ExtendedManager()


class Worker(SelfValidationMixin, GetFieldRelatedNameMixin, models.Model):
    validators = [validate_add_worker_data_to_user]

    exp = models.IntegerField(blank=True, null=True)
    speciality = models.CharField(max_length=50, null=True, blank=True, verbose_name="Специальность")
    education = models.CharField(max_length=50, null=True, blank=True, verbose_name="Образование")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker')


class Customer(SelfValidationMixin, GetFieldRelatedNameMixin, models.Model):
    validators = [validate_add_worker_data_to_user]

    class LegalType(models.TextChoices):
        ENTITY = "entity", "Entity"
        PERSON = "person", "Person"

    discount = models.IntegerField(blank=True, null=True)
    legal = models.CharField(max_length=50, choices=LegalType, default=LegalType.PERSON)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
