from rest_framework import serializers
from .models import HelpResource


class HelpResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpResource
        fields = ['id', 'name', 'description', 'url', 'location', 'category', 'phone']