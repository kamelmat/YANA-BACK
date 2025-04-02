from django.contrib import admin
from django.urls import path, include
from apps.users.api.api import UserAPIVew

urlpatterns = [
    path("usuario/",UserAPIVew.as_view(), name = "usuario_api" )
]