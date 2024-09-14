from rest_framework import serializers
from .models import Task


class TaskReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['title', 'customer', 'worker']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['report', 'worker']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['title', 'customer', 'worker']


class TaskPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['report', 'status', 'worker']


# class JobSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'
#         read_only_fields = ['title', 'customer', 'worker']
#
#     def create(self, validated_data):
#         raise serializers.ValidationError({'Error': 'у мужлан нет прав'})
#
#     def update(self, instance, validated_data):
#         user = self.context["request"].user
#         instance.worker = user.worker
#         return super().update(instance, validated_data)
#
#
# class JobCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'
#
#
# class TaskSerializer(serializers.ModelSerializer):
#     customer = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Task
#         fields = '__all__'
#         read_only_fields = ['report', 'status', 'worker']
#
#     def save(self, **kwargs):
#         user = self.context["request"].user
#         if user.type == "customer":
#             kwargs['customer'] = user.customer
#
#         return super().save(**kwargs)