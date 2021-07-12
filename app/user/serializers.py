from trader.serializers import AlgorithmSerializer
from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    selected_algo = AlgorithmSerializer()
    
    class Meta:
        model = User
        fields = ('username','id','daily_emails','selected_algo','daily_emails')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)
        validated_data.pop('message', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password','email','first_name','last_name')