from rest_framework import routers

from chat import viewsets

router = routers.DefaultRouter()
router.register(r'chats', viewsets.ChatViewSet, basename='chats')
