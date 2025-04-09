from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from .models import Emotion, SharedEmotion
from .serializers import *
from rest_framework.response import Response
import math

#emociones que gestionamos desde el admin:
class EmotionListView(generics.ListAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    permission_classes = [AllowAny]

class CreateEmotionView(generics.CreateAPIView):
    serializer_class = EmotionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class EmotionBulkCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmotionSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = EmotionSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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
        return SharedEmotion.objects.filter(user=self.request.user).order_by('-timestamp')

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

        nearby = []
        for ue in UserEmotion.objects.select_related('emotion').all():
            distance = haversine(lat, lon, ue.latitude, ue.longitude)
            if distance <= radius_km:
                nearby.append({
                    'emotion_id': ue.emotion.id,
                    'emotion_name': ue.emotion.name,
                    'latitude': ue.latitude,
                    'longitude': ue.longitude,
                })

        return Response(nearby, status=status.HTTP_200_OK)