from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.users.api.serializers import UserSerializer

class UserAPIVew(APIView):
    def get(self, request):
        user = User.objects.all()
        user_serializer = UserSerializer(user, many = True)
        return Response(user_serializer.data)