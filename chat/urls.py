from rest_framework import routers
from .views import TopicView, MessageView
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'topics', TopicView, basename='topics')
router.register(r'messages', MessageView, basename='messages')


urlpatterns = [
    path('api/', include(router.urls)),
    #path('', home, name="home"),
]