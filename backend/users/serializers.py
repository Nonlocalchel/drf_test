from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *
from .utils import clean_user_input_data


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

    def create(self, validated_data):
        return clean_user_input_data(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['type'] = user.type
        return token
