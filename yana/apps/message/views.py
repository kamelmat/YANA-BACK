from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SupportMessageTemplate

class SupportTemplatesView(APIView):
    def get(self, request):
        templates = SupportMessageTemplate.objects.all()
        return Response([{'id': t.id, 'text': t.text} for t in templates], status=status.HTTP_200_OK)
