from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    #customer = serializers.HiddenField(default=serializers.CurrentUserDefault())#для заказчика
    class Meta:
        model = Task
        fields = ['id', 'title', 'time_create', 'time_close', 'status', 'customer', 'worker']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'worker']