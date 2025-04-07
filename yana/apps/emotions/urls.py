from django.urls import path
from .views import *

urlpatterns = [
    
    path('user/emotions/bulk/', EmotionBulkCreateView.as_view(), name='user-emotion-bulk-create'),
    path('user/emotions/', EmotionListView.as_view(), name='emotion-list'),
    path('user/emotions/list', UserEmotionListView.as_view(), name='user-emotions')
]


