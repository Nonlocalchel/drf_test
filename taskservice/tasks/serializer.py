from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    #customer = serializers.HiddenField(default=serializers.CurrentUserDefault())#для заказчика
    class Meta:
        model = Task
        fields = ['id', 'title', 'time_create', 'time_close', 'status', 'customer', 'worker']


class TaskReportUpdateSerializer(serializers.Serializer):
    status = serializers.HiddenField(default='done')
    report = serializers.CharField()

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.report = validated_data.get("report", instance.report)
        instance.clean()
        instance.save()
        return instance


class TaskCloseSerializer(serializers.Serializer):
    status = serializers.HiddenField(default='done')
    report = serializers.CharField()

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.report = validated_data.get("report", instance.report)
        instance.clean()
        instance.save()
        return instance


