from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    volume = models.PositiveBigIntegerField(blank=True, null=True)
    exchange=models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker

class Algorithm(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True,null=True)
    public = models.BooleanField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Decision(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    openPrice = models.FloatField()
    closingPrice = models.FloatField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    tradeDate= models.DateField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.stock) + ' on ' + str(self.tradeDate)