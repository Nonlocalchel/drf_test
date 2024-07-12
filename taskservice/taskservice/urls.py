"""
URL configuration for taskservice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from tasks.views import *
from users.views import *

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'workers', WorkerViewSet, basename='workers')
router.register(r'customers', CustomersViewSet, basename='customers')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls))
]

admin.site.site_header = "Панель админа"
admin.site.index_title  = "Сервис работ"