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
        try:
            lat = float(request.query_params.get('latitude'))
            lon = float(request.query_params.get('longitude'))
            radius_km = float(request.query_params.get('radius', 5))  # default 5km
        except (TypeError, ValueError):
            return Response({'error': 'Parámetros inválidos'}, status=status.HTTP_400_BAD_REQUEST)

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
                math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
            return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

        user_last_emotion = None
        if request.user.is_authenticated:
            last_emotion = SharedEmotion.objects.filter(
                user=request.user,
                is_active=True
            ).order_by('-created_at').first()
            if last_emotion:
                user_last_emotion = last_emotion.emotion

        shared_emotions = SharedEmotion.objects.select_related('emotion').filter(
            is_active=True
        ).exclude(user=request.user) if request.user.is_authenticated else SharedEmotion.objects.select_related('emotion').filter(is_active=True)
        
        latest_emotions = {}
        for se in shared_emotions.order_by('-created_at'):
            if se.user_id not in latest_emotions:
                if not user_last_emotion or se.emotion == user_last_emotion:
                    latest_emotions[se.user_id] = se
        
        nearby = []
        for se in latest_emotions.values():
            distance = haversine(lat, lon, se.latitude, se.longitude)
            if distance <= radius_km:
                nearby.append({
                    'emotion_id': se.emotion.id,
                    'emotion': se.emotion.name,
                    'latitude': se.latitude,
                    'longitude': se.longitude,
                    'user_id': se.user.user_id,
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