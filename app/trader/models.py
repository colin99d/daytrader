from datetime import datetime, date, timedelta, time
from django.utils import timezone
from django.db import models
import requests

def last_date(dt):
    holidays = [date(2021,7,5),date(2021,9,6),date(2021,12,24),date(2022,1,17),date(2022,2,21),date(2022,4,15),date(2022,5,30),date(2022,7,4),
        date(2022,9,5),date(2022,12,26),date(2023,1,2),date(2023,1,16),date(2023,2,20),date(2023,4,7),date(2023,5,29),date(2023,7,4),
        date(2023,9,4),date(2023,12,25)]
    if dt.date() in holidays:
        dt = dt - timedelta(days=1)
    weekday = dt.weekday()
    currTime = dt.time()
    if weekday == 5:
        lastDate = (dt - timedelta(days=1)).date()
        close = True
    elif weekday == 6:
        lastDate = (dt - timedelta(days=2)).date()
        close = True
    else:
        if currTime > time(16,0,0):
            lastDate = dt.date()
            close = True
        elif currTime > time(9,30,0):
            lastDate = dt.date()
            close = False
        else:
            lastDate = (dt - timedelta(days=1)).date()
            close = True
    return lastDate, close

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
        url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'+ self.ticker +'?modules=price'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        query = requests.get(url, headers=headers)
        try:
            if self.listed or self.listed is None:
                response = query.json()
                clean = response["quoteSummary"]["result"][0]["price"]
                last_updated = datetime.fromtimestamp(clean["regularMarketTime"])
                open_price = clean["regularMarketOpen"]["raw"]
                volume = clean["regularMarketVolume"]["raw"]
                setattr(self,"last_updated",last_updated)
                setattr(self,"price",open_price)
                setattr(self,"volume",volume)
                if last_updated.date() >= last_date(timezone.now())[0]:
                    setattr(self,"active",(volume > 0))
                    setattr(self,"listed",(volume > 0))
                else:
                    setattr(self,"active",False)
                    setattr(self,"listed",False)
        except TypeError:
            if response["quoteSummary"]['error']['code'] == 'Not Found':
                setattr(self,"active",False)
                setattr(self,"listed",False)
        except KeyError:
            setattr(self,"active",False)
            setattr(self,"listed",False)
        except ValueError:
            setattr(self,"active",False)
            setattr(self,"listed",False)
        self.save()

    def get_cashflows(self, quarterly=False):
        ending = "cashflowStatementHistoryQuarterly" if quarterly else "cashflowStatementHistory"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ self.ticker.upper() +'?modules='+ending
        response = requests.get(url, headers=headers).json()
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

    def get_info(self):
        url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'+ self.ticker +'?modules=price'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        query = requests.get(url, headers=headers)
        response = query.json()
        try:
            clean = response["quoteSummary"]["result"][0]["price"]
            last_updated = datetime.fromtimestamp(clean["regularMarketTime"])
            open_price = clean["regularMarketPrice"]["raw"]
            volume = clean["regularMarketVolume"]["raw"]
            return {"time":last_updated, "price":open_price, "volume":volume}
        except TypeError:
            return None

    def get_options_chain(self):
        pass

class Algorithm(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True,null=True)
    public = models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Decision(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    open_price = models.FloatField(null=True, blank=True)
    closing_price = models.FloatField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    trade_date= models.DateField()
    long = models.BooleanField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.stock) + ' on ' + str(self.trade_date)

    class Meta:
        ordering = ['created_at']