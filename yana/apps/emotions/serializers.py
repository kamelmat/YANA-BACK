from rest_framework import serializers
from .models import *

class EmotionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Emotion
        fields = ['id', 'name', 'image']



