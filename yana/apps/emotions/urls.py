from django.urls import path
from .views import *

urlpatterns = [
    #emociones que gestionamos desde el admin:
    path('user/emotions/bulk/', EmotionBulkCreateView.as_view(), name='emotion-bulk-create'),
    path('user/available/emotions/', EmotionListView.as_view(), name='emotion-list'),
    
    #emociones que agrega/elimina el usuario:
    path('user/emotions/create/', UserCreateEmotionView.as_view(), name='user-create-emotion'),
]
