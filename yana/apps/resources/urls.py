from django.urls import path
from .views import HelpResourceListCreateView, HelpResourceDetailView

urlpatterns = [
    path('api/resources/', HelpResourceListCreateView.as_view(), name='resource-list'),
    path('api/resources/<int:pk>/', HelpResourceDetailView.as_view(), name='resource-detail'),
]
