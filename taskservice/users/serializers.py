from rest_framework import serializers
from .models import *


class UserReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ["password", "last_login", "groups", "user_permissions"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'username', 'phone', 'password', 'password2')

    def validate(self, attrs):
        data = super(UserCreateSerializer, self).validate(attrs)
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password mismatch')
        del data['password2']
        return data

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['exp', 'is_super_worker']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class UserWorkerSerializer(UserReadSerializer):
    worker = WorkerSerializer(many=False, read_only=True)


class UserCustomerSerializer(UserReadSerializer):
    customer = CustomerSerializer(many=False, read_only=True)