from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *
from .utils import get_user_types


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['pk', 'exp', 'speciality', 'education']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['pk', 'discount', 'legal']


class UserSerializer(WritableNestedModelSerializer):
    password = serializers.CharField(write_only=True)

    worker = WorkerSerializer(allow_null=True, default=None)

    customer = CustomerSerializer(allow_null=True, default=None)

    def get_fields(self):
        fields = super().get_fields()
        instance = self.instance
        action = self._context['view'].action
        if action != 'list':
            user_types = get_user_types()
            create_user_type = instance.type
            for user_type in user_types:
                if user_type == create_user_type:
                    continue

                fields.pop(user_type)

        return fields

    class Meta:
        model = User
        fields = (
            'pk',
            'username', 'phone', 'is_staff',
            'type', 'email',
            'first_name', 'last_name', 'is_superuser',
            'worker', 'customer', 'photo',
            'password'
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['type'] = user.type
        return token
