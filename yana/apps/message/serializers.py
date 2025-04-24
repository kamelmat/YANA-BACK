from rest_framework import serializers
from .models import *
from apps.emotions.models import SharedEmotion

class SendSupportMessageSerializer(serializers.Serializer):
    shared_emotion = serializers.PrimaryKeyRelatedField(queryset=SharedEmotion.objects.all())
    template_id = serializers.PrimaryKeyRelatedField(
        queryset=SupportMessageTemplate.objects.all(),
        write_only=True  # This field is only for input
    )

    def create(self, validated_data):
        # Remove shared_emotion from validated_data as it's not a field in SupportMessage
        shared_emotion = validated_data.pop('shared_emotion', None)
        template = validated_data.pop('template_id', None)
        
        # Create the message with the template text
        return SupportMessage.objects.create(
            message=template.text,
            **validated_data
        )

class SupportMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = ['message', 'created_at']

class SupportMessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessageTemplate
        fields = ['id', 'text']