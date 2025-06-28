from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'data-sources', views.DataSourceViewSet, basename='data_sources')
router.register(r'conversations', views.ConversationViewSet, basename='conversations')
router.register(r'conversation-notes', views.ConversationNoteViewSet, basename='conversation-notes')
router.register(r'messages', views.MessageViewSet, basename='messages')
router.register(r'spaces', views.SpaceViewSet, basename='spaces')
router.register(r'tags', views.TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
]
