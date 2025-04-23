# apps/message/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Admin views
    path('admin/templates/create/', CreateSupportTemplateView.as_view(), name='create-template'),
    path('admin/templates/delete/<int:pk>/', DeleteSupportTemplateView.as_view(), name='delete-template'),

    # Message list view
    path('templates/', SupportTemplatesView.as_view(), name='support-templates'),

    # API endpoints
    path('api/send-support/', SendSupportMessageView.as_view(), name='send-support'),
    path('api/received-messages/', ReceivedSupportMessagesView.as_view(), name='received-messages'),
    path('api/notifications/', NotificationsView.as_view(), name='notifications'),
    path('api/messageasread/', MessagesAsReadView.as_view(), name='message-as-read'),
]

