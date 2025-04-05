from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Emotion
from .serializers import *

class EmotionListView(generics.ListAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    permission_classes = [AllowAny]

class UserEmotionCreateView(generics.CreateAPIView):
    serializer_class = UserEmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserEmotionListView(generics.ListAPIView):
    serializer_class = UserEmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserEmotion.objects.filter(user=self.request.user).order_by('-timestamp')

