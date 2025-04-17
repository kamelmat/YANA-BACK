from django.contrib.auth.models import *
from django.contrib.auth.forms import *
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from rest_framework import serializers 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        error_messages={
            "min_length": "La contraseña debe tener al menos 8 caracteres."
        }
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        """Validar contraseña con reglas personalizadas"""
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("La contraseña debe incluir al menos un número.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("La contraseña debe incluir al menos una letra mayúscula.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("La contraseña debe incluir al menos una letra minúscula.")
        if not any(char in "!@#$%^&*()-_+=<>?/{}[]" for char in value):
            raise serializers.ValidationError("La contraseña debe incluir al menos un carácter especial (!@#$%^&* etc.)")
        
        validate_password(value)  # Usa validadores de Django
        
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            last_name=validated_data['last_name'],
           
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
                'user_id': self.user.user_id,
                'name': self.user.name,
                'avatar_id': self.user.avatar_id
            }
        })
        return data
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        try: 
            refresh_token = attrs["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError(f"Invalid refresh token: {str(e)}")

        return attrs

class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError("Incorrect password")
        return attrs

class UpdateAvatarSerializer(serializers.Serializer):
    avatar_id = serializers.IntegerField(min_value=31, max_value=35)