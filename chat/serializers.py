from rest_framework import serializers
from .models import Topic, Message

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()
    same_user = serializers.SerializerMethodField('same_user')

    def same_user(self,request):
        return self.user == request.user
        
    class Meta:
        model = Message
        fields = ('text','topic','user','same_user')
        read_only_fields = ['same_user']