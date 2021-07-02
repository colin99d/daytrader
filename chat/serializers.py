from rest_framework import serializers
from .models import Topic, Message

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()
    same = serializers.SerializerMethodField('same')

    def same(self,request):
        return self.user == request.user
        
    class Meta:
        model = Message
        fields = '__all__'