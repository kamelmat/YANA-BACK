from django.contrib import admin
from django.urls import path, include
from apps.users.views import UserAPIView
from apps.users.views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/generate-user-id/', GenerateUserIDView.as_view(), name='generate_user_id'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('admin/users/', UserAPIView.as_view(), name='user-list'),
    path('api/user/details/', UserDetailView.as_view(), name='user-detail'),
    path('api/check-email/', EmailCheckView.as_view(), name='check-email'),
    path('api/delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('api/update-avatar/', UpdateAvatarView.as_view(), name='update-avatar'),
]
