from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, generics
from .models import SupportMessageTemplate, SupportMessage
from .serializers import *

class SupportTemplatesView(APIView):
    def get(self, request):
        templates = SupportMessageTemplate.objects.all()
        return Response([{'id': t.id, 'text': t.text} for t in templates], status=status.HTTP_200_OK)

class SendSupportMessageView(generics.CreateAPIView):
    serializer_class = SendSupportMessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shared_emotion = serializer.validated_data['shared_emotion']
        sender = request.user
        receiver = shared_emotion.user

        if sender == receiver:
            return Response(
                {"detail": "No puedes enviarte un mensaje de apoyo a ti mismo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the message using serializer.save()
        serializer.save(sender=sender, receiver=receiver)

        receiver.unread_messages = True
        receiver.save()

        return Response({"message": "Mensaje de apoyo enviado"}, status=status.HTTP_201_CREATED)
    
class ReceivedSupportMessagesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupportMessagesSerializer

    def get_queryset(self):
         return SupportMessage.objects.filter(receiver=self.request.user).order_by('-created_at')
    
class CreateSupportTemplateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SupportMessageTemplateSerializer
    
    def perform_create(self, serializer):
        serializer.save()

class DeleteSupportTemplateView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SupportMessageTemplateSerializer
    queryset = SupportMessageTemplate.objects.all()

class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    # Verificar si el usuario tiene mensajes no leídos

    def get(self, request):
        user = request.user
        return Response(user.unread_messages, status=status.HTTP_200_OK)
    
class MessagesAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    # Marcar los mensajes como leídos

    def post(self, request):
        user = request.user
        user.unread_messages = False
        user.save()
        return Response(status=status.HTTP_200_OK)
