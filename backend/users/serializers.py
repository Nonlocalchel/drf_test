from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import *
from .utils import figure_deleted_data


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

    worker = WorkerSerializer(allow_null=True, default=None)

    customer = CustomerSerializer(allow_null=True, default=None)

    class Meta:
        model = User
        fields = (
            'pk',
            'username', 'phone', 'is_staff',
            'type', 'email',
            # 'first_name', 'last_name', 'is_superuser',
            'worker', 'customer', 'photo',
            'password'
        )

    def create(self, validated_data):
        user_type = validated_data.get('type')
        deleted_key = figure_deleted_data(user_type)
        validated_data.pop(deleted_key, None)
        return super().create(validated_data)
