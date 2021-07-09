from datetime import datetime
from django.db import models
import requests

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    volume = models.PositiveBigIntegerField(blank=True, null=True)
    exchange=models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)
    listed = models.BooleanField(null=True, default=None)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker

    def update_stock_info(self):
        ticker = self.ticker
        url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ ticker +'?modules=price'
        response = requests.get(url).json()["quoteSummary"]
        try:
            if self.listed == True or self.listed == None:
                clean = response["result"][0]["price"]
                last_updated = datetime.fromtimestamp(clean["regularMarketTime"])
                openPrice = clean["regularMarketOpen"]["raw"]
                volume = clean["regularMarketVolume"]["raw"]
                setattr(self,"last_updated",last_updated)
                setattr(self,"price",openPrice)
                setattr(self,"volume",volume)
                setattr(self,"active",(volume > 0))
                setattr(self,"listed",True)
        except TypeError:
            if response['error']['code'] == 'Not Found':
                setattr(self,"active",False)
                setattr(self,"listed",False)
        except KeyError:
                setattr(self,"active",False)
                setattr(self,"listed",False)
        self.save()

    def get_cashflows(self, quarterly=False):
        ending = "cashflowStatementHistory" if quarterly == False else "cashflowStatementHistoryQuarterly"
        url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ self.ticker.upper() +'?modules='+ending
        response = requests.get(url).json()
        try:
            items = response['quoteSummary']['result'][0][ending]['cashflowStatements']
            dictVals = [{"id": "Operating Cash Flows", "data": []},{"id": "Financing Cash Flows", "data": []},{"id": "Investing Cash Flows", "data": []}]
            for item in items:
                date = datetime.utcfromtimestamp(item['endDate']['raw']).strftime("%m-%d-%Y")
                dictVals[0]["data"].append({"x":date,"y":item['totalCashFromOperatingActivities']['raw']})
                dictVals[1]["data"].append({"x":date,"y":item['totalCashFromFinancingActivities']['raw']})
                dictVals[2]["data"].append({"x":date,"y":item['totalCashflowsFromInvestingActivities']['raw']})    
            return dictVals
        except TypeError:
            return {"Error": "Ticker does not have an available statement of cash flows"}

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
    long = models.BooleanField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.stock) + ' on ' + str(self.tradeDate)