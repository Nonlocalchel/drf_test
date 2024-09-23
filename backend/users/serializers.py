from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            'username', 'phone',
            'photo', 'type', 'email',
            'first_name', 'last_name', 'is_super_user',
            'password'
        )

#
# class UserReadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ["password", "last_login", "groups", "user_permissions"]
#
#
# class WorkerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Worker
#         fields = ['exp', 'is_super_worker']
#
#
# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = "__all__"
#
#
# class UserWorkerSerializer(UserReadSerializer):
#     worker = WorkerSerializer(many=False, read_only=True)
#
#
# class UserCustomerSerializer(UserReadSerializer):
#     customer = CustomerSerializer(many=False, read_only=True)
