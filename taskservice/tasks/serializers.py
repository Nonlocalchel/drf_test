from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['title', 'customer', 'worker']



    # def update(self, instance, validated_data):


# class WorkerTaskCreateSerializer(serializers.ModelSerializer):


#
# class CustomerTaskCreateSerializer(serializers.ModelSerializer):
#     customer = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Task
#         fields = '__all__'
#
#     def save(self, **kwargs):
#         user = self.context["request"].user
#         if user.type == "customer":
#             kwargs['customer'] = user.customer
#
#         return super().save(**kwargs)
#
#
# class WorkerTaskCreateSerializer(serializers.ModelSerializer):
#     customer = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Task
#         fields = '__all__'
#
#
# class TaskUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'
#         read_only_fields = ("title", )

# class TaskCreateSerializer(serializers.ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     customer = serializers.SerializerMethodField(allow_null=True)
#
#     class Meta:
#         model = Task
#         fields = '__all__'
#
#     def get_customer(self, obj):
#         print(self.context["request"])
#         print(obj)
#         user = self.context["request"].user
#         if user.type == "customer":
#             return user.customer