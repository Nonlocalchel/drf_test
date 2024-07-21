from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    # customer = serializers.HiddenField(default=serializers.CurrentUserDefault())#для заказчика
    class Meta:
        model = Task
        fields = "__all__"

