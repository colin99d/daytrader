from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.ticker

class Algorithm(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DecisionHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    openPrice = models.FloatField()
    closingPrice = models.FloatField(null=True, blank=True)
    confidence = models.FloatField()
    tradeDate= models.DateTimeField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.stock) + ' on ' + str(self.tradeDate)