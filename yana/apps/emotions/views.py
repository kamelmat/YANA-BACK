from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from .models import Emotion, SharedEmotion
from .serializers import *
from rest_framework.response import Response
import math
from .permissions import IsAdminUser
from django.db.models import Count
from django.db import models

#emociones que gestionamos desde el admin:
class EmotionListView(generics.ListAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    permission_classes = [AllowAny]

class CreateEmotionView(generics.CreateAPIView):
    serializer_class = EmotionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()

class EmotionBulkCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = EmotionSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = EmotionSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class DeleteEmotionView(generics.DestroyAPIView):
    queryset = Emotion.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = EmotionSerializer


#emociones que agrega el usuario:
class UserCreateEmotionView(generics.CreateAPIView):
    serializer_class = SharedEmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SharedEmotionListView(generics.ListAPIView):
    serializer_class = SharedEmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SharedEmotion.objects.filter(user=self.request.user).order_by('-created_at')

#Emociones geospaciales
class NearbyEmotionsView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get user's last emotion
        last_emotion = SharedEmotion.objects.filter(
            user=request.user,
            is_active=True
        ).order_by('-created_at').first()

        if not last_emotion:
            return Response({'error': 'No emotions found for user'}, status=status.HTTP_404_NOT_FOUND)

        # Get the latest emotion for each user (including the requesting user)
        latest_emotions = {}
        all_emotions = SharedEmotion.objects.filter(
            is_active=True
        ).select_related('emotion', 'user').order_by('-created_at')

        for se in all_emotions:
            if se.user_id not in latest_emotions:
                latest_emotions[se.user_id] = se

        # Filter out emotions that don't match the user's emotion
        matching_emotions = [se for se in latest_emotions.values() if se.emotion == last_emotion.emotion]

        # Serialize the results
        nearby = []
        for se in matching_emotions:
            nearby.append({
                'shared_emotion_id': se.id,
                'emotion_id': se.emotion.id,
                'emotion': se.emotion.name,
                'latitude': se.latitude,
                'longitude': se.longitude,
                'user_id': se.user.id,
                'created_at': se.created_at
            })

        return Response(nearby, status=status.HTTP_200_OK)
    

class GlobalEmotionsSummaryView(APIView):
        def get(self, request):
            emotion_counts = (
            SharedEmotion.objects
            .filter(is_active=True)
            .values('emotion__name')
            .annotate(count=Count('id'))
        )

            result = {item['emotion__name']: item['count'] for item in emotion_counts}
            return Response(result)

class LastUserEmotionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        last_emotion = SharedEmotion.objects.filter(
            user=request.user,
            is_active=True
        ).order_by('-created_at').first()
        
        if not last_emotion:
            return Response(
                {'detail': 'No emotions found for this user'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = SharedEmotionSerializer(last_emotion)
        return Response(serializer.data)