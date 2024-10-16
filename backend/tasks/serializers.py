from rest_framework import serializers
from .models import Task


class TaskReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['report', 'worker']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['report', 'customer', 'worker', 'status']


class TaskPartialUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Task.StatusType)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['title', 'customer']
