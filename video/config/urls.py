#coding:utf-8

from django.contrib import admin
from django.urls import path, include
from apps.dashboard import urls as dashboard_urls
from apps.client import urls as client_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include(dashboard_urls)),
    path('client/', include(client_urls))
]
