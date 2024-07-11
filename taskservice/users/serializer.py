from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active",
                  "phone", "photo", "type"]


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['exp']


class UserWorkerSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'worker']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['discount']


class UserCustomerSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'customer']