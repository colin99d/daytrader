from .serializers import TopicSerializer, MessageSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .models import Topic, Message

class MessagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


# Create your views here.
class TopicView(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    pagination_class = MessagePagination

    def get_queryset(self):
        topicID = self.request.GET.get('topic', None)
        if topicID:
            topic = Topic.objects.get(pk=topicID)
            return Message.objects.filter(topic=topic)
        else:
            return None