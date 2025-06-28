from django.urls import path, include
from rest_framework import routers

from accounts import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'keys', views.AuthTokenViewSet, basename='tokens')
router.register(r'organizations', views.OrganizationViewSet, basename='organizations')

urlpatterns = [
    path('', include(router.urls)),
    path(r'tokens/create/', views.AuthTokenCreateView.as_view(), name='account_token'),

    path('auth/webhook/', views.auth_webhook_handler, name='auth-user-created-webhook'),
]
