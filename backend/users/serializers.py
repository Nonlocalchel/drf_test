from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *
from .utils import fix_serializer_fields, format_repr, get_instance_type


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

    def get_fields(self):
        """Eliminates unnecessary profile data requests"""
        fields = super().get_fields()
        instance = self.instance
        if instance is None:
            fixed_fields = fix_serializer_fields(instance, fields, data=self.initial_data)
        else:
            fixed_fields = fix_serializer_fields(instance, fields)

        return fixed_fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_type = get_instance_type(instance)
        formatted_representation = format_repr(representation, user_type)
        return formatted_representation


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['type'] = user.type
        return token
