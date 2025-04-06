from django.urls import path
from .views import *

urlpatterns = [
    path('emotions/', EmotionListView.as_view(), name='emotion-list'),
    path('user/emotions/', EmotionListView.as_view(), name='user-emotion-list'),
    path('user/emotions/new/', CreateEmotionView.as_view(), name='user-emotion-create'),
    path('user/emotions/bulk/', EmotionBulkCreateView.as_view(), name='user-emotion-bulk-create'),
]


