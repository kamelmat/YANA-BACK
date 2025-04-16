from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import HelpResource
from .serializers import HelpResourceSerializer

class HelpResourceListCreateView(generics.ListCreateAPIView):
    queryset = HelpResource.objects.all()
    serializer_class = HelpResourceSerializer

class HelpResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HelpResource.objects.all()
    serializer_class = HelpResourceSerializer