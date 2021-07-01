from .models import Stock, Algorithm, Decision
from rest_framework import serializers

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = '__all__'

class DecisionGetSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    algorithm = AlgorithmSerializer()
    class Meta:
        model = Decision
        fields = '__all__'

class DecisionSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    algorithm = AlgorithmSerializer()
    class Meta:
        model = Decision
        fields = '__all__'