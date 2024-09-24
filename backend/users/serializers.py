from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from .models import *


class WorkerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = Worker
        fields = '__all__'
        read_only = ['user']


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = Customer
        fields = '__all__'


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
