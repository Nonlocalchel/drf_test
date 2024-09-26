import os

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import *


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['pk', 'exp', 'is_super_worker']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['pk', 'discount', 'is_super_customer']


class UserSerializer(WritableNestedModelSerializer):
    password = serializers.CharField(write_only=True)  # , style={'input_type': 'password'}
    worker = WorkerSerializer(allow_null=True)
    customer = CustomerSerializer(allow_null=True)
    # photo = serializers.SerializerMethodField()

    # os.path.join(MEDIA_ROOT, menu.img.url)

    class Meta:
        model = User
        fields = (
            'pk',
            'username', 'phone',
            'photo', 'type', 'email',
            'first_name', 'last_name', 'is_superuser',
            'worker', 'customer',
            'password'
        )