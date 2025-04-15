# apps/message/urls.py
from django.urls import path
from .views import SupportTemplatesView

urlpatterns = [
    path('templates/', SupportTemplatesView.as_view(), name='support-templates'),
]
