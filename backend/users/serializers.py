from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from .models import *


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        exclude = ['user']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['user']


class UserSerializer(WritableNestedModelSerializer):
    password = serializers.CharField(write_only=True)  # , style={'input_type': 'password'}
    worker = WorkerSerializer(allow_null=True)
    customer = CustomerSerializer(allow_null=True)

    class Meta:
        model = User
        fields = (
            'username', 'phone',
            'photo', 'type', 'email',
            'first_name', 'last_name', 'is_superuser',
            'worker', 'customer',
            'password'
        )
