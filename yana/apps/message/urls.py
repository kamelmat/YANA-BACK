# apps/message/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('templates/', SupportTemplatesView.as_view(), name='support-templates'),
    path('api/send-support/', SendSupportMessageView.as_view(), name='send-support'),
    path('api/received-messages/', ReceivedSupportMessagesView.as_view(), name='received-messages'),
    path('admin/templates/create/', CreateSupportTemplateView.as_view(), name='create-template'),
    path('admin/templates/delete/<int:pk>/', DeleteSupportTemplateView.as_view(), name='delete-template')
]
