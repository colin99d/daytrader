from rest_framework.permissions import IsAuthenticated 
from .models import Stock, Algorithm, Decision
from rest_framework import serializers


class StockSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,) 

    class Meta:
        model = Stock
        fields = '__all__'

class AlgorithmSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)

    class Meta:
        model = Algorithm
        fields = '__all__'

class DecisionGetSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,) 
    stock = StockSerializer()
    algorithm = AlgorithmSerializer()

    class Meta:
        model = Decision
        fields = '__all__'

class DecisionSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,) 
    
    class Meta:
        model = Decision
        fields = '__all__'