from django.urls import path
from .views import *

urlpatterns = [
    #emociones que gestionamos desde el admin:
    path('admin/emotions/bulk/', EmotionBulkCreateView.as_view(), name='emotion-bulk-create'),
    path('admin/emotions/create/', CreateEmotionView.as_view(), name='emotion-create'),
    path('admin/emotions/delete/<int:pk>/', DeleteEmotionView.as_view(), name='emotion-delete'),

    # emociones disponibles para todos (sin autenticación)
    path('emotions/available/', EmotionListView.as_view(), name='emotion-list'),
    
    #emociones que agrega/elimina el usuario:
    path('user/emotions/create/', UserCreateEmotionView.as_view(), name='user-create-emotion'),
    path('user/emotions/', SharedEmotionListView.as_view(), name='user-emotion-list'),
    
    #emociones cercanas
    path('api/nearby-emotions/', NearbyEmotionsView.as_view(), name='nearby_emotions'),
    path('api/global-emotions/', GlobalEmotionsSummaryView.as_view(), name='global-emotions-summary'),

]
