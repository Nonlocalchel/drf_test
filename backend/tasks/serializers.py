from rest_framework import serializers
from .models import Task


class TaskReadSerializer(serializers.ModelSerializer):
    """Task serializer class for read data"""
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    """Task serializer class for create data"""
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['report', 'worker']


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Task serializer class for update(put) data"""
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['report', 'customer', 'worker', 'status']


class TaskPartialUpdateSerializer(serializers.ModelSerializer):
    """Task serializer class for partial update(patch) data"""
    status = serializers.ChoiceField(choices=Task.StatusType)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['title', 'customer']
