from django.urls import path
from .views import *

urlpatterns = [
    #emociones que gestionamos desde el admin:
    path('user/emotions/bulk/', EmotionBulkCreateView.as_view(), name='emotion-bulk-create'),
    path('user/available/emotions/', EmotionListView.as_view(), name='emotion-list'),
    
    path('user/emotions/bulk/', EmotionBulkCreateView.as_view(), name='user-emotion-bulk-create'),
    path('user/emotions/', EmotionListView.as_view(), name='emotion-list'),
    path('user/emotions/list', UserEmotionListView.as_view(), name='user-emotions')
    #emociones que agrega/elimina el usuario:
    path('user/emotions/create/', CreateEmotionView.as_view(), name='create-emotion'),

]


