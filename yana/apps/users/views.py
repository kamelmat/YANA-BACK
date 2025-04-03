from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.users.serializers import UserSerializer
from apps.users.models import *
from apps.users.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


class UserAPIVew(APIView):
    def get(self, request):
        user = User.objects.all()
        user_serializer = UserSerializer(user, many = True)
        return Response(user_serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class GenerateUserIDView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = generate_unique_user_id()
        return Response({'user_id': user_id})
    
class LoginView(TokenObtainPairView):
    
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Logout successful"})
