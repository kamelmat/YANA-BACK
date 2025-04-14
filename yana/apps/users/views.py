from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.users.serializers import UserSerializer
from apps.users.models import *
from apps.users.serializers import *
from apps.users.utils import generate_unique_user_id
from django.shortcuts import get_object_or_404

class UserAPIVew(APIView):
        
    def get(self, request):
        user = CustomUser.objects.all()
        user_serializer = UserSerializer(user, many = True)
        return Response(user_serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Guarda el usuario
        
        # Generar tokens para el usuario recién creado
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response_data = {
            "user_id": user.user_id,
            "email": user.email,
            "name": user.name,
            "last_name": user.last_name,
            "date_joined": user.date_joined,
            "access_token": access_token,
            "refresh_token": str(refresh),
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)

class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class GenerateUserIDView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = generate_unique_user_id()
        return Response({'user_id': user_id})
    
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class EmailCheckView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {"error": "Email is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email_exists = CustomUser.objects.filter(email=email).exists()
        return Response(
            {"email_exists": email_exists},
            status=status.HTTP_200_OK
        )

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.delete()
            return Response(
                {"message": "Account successfully deleted"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
