from .serializers import TopicSerializer, MessageSerializer
from rest_framework import viewsets
from .models import Topic, Message


# Create your views here.
class TopicView(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()