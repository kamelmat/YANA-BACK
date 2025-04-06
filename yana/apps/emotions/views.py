from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Emotion
from .serializers import *
from rest_framework.response import Response

class EmotionListView(generics.ListAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    permission_classes = [AllowAny]

"""""
class UserEmotionCreateView(generics.CreateAPIView):
    serializer_class = EmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
"""
"""class UserEmotionListView(generics.ListAPIView):
    serializer_class = EmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Emotion.objects.filter(user=self.request.user).order_by('-timestamp')
"""
class CreateEmotionView(generics.CreateAPIView):
    serializer_class = EmotionSerializer

    def perform_create(self, serializer):
        serializer.save()

class EmotionBulkCreateView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = EmotionSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)