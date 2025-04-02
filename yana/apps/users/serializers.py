from django.contrib.auth.models import *
from django.contrib.auth.forms import *
from django.shortcuts import render, redirect
from rest_framework import serializers 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.models import *

class UserSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user': {
                'email': self.user.email,
            }
        })
        return data