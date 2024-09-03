from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register(r'workers', WorkerViewSet, basename='workers')
router.register(r'customers', CustomersViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls))

]
