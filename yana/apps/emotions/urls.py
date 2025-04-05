from django.urls import path
from .views import *

urlpatterns = [
    path('emotions/', EmotionListView.as_view(), name='emotion-list'),
    path('user/emotions/', UserEmotionListView.as_view(), name='user-emotion-list'),
    path('user/emotions/new/', UserEmotionCreateView.as_view(), name='user-emotion-create'),
]


