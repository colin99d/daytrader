from trader.functions.scrapers import valid_ticker, get_stock_info
from trader.functions.helpers import last_date
from trader.templatetags.filter import growth
from django.utils.timezone import make_aware
from django.test import TransactionTestCase
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import status
from django.urls import reverse
from trader.models import Stock
import random

class HelpersTestCase(TransactionTestCase):

    def test_view_home(self):
        """Tests that home provides a basic repsonse"""
        response = self.client.get('', follow=True)
        self.assertTrue("This is the base URL for the daytrading API" in response.content.decode("utf-8") )

    def test_function_valid_ticker(self):
        """Test that the ticker function properly classifies strings"""
        self.tickers = ["AAPL","TSLA","XYZZY","ZZZ","IWV","AMZN","NARP","WEEN"]
        truthVals = [valid_ticker(x) for x in self.tickers]
        self.assertEqual(truthVals, [True,True,False,False,True,True,False,False])

    def test_view_get_cashflows(self):
        """Ensures that the get_cashflow function response returns json"""
        response = self.client.post(reverse("cashflows"),{'ticker':'AAPL'}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.json()[0].keys())

    def test_stock_date_analyzer(self):
        """Tests that the formula that classifies dates in stock market terms works"""
        date1 = make_aware(datetime(2021, 6, 5, 12, 0))
        date2 = make_aware(datetime(2021, 6, 6, 12, 0))
        date3 = make_aware(datetime(2021, 6, 7, 20, 0))
        date4 = make_aware(datetime(2021, 6, 8, 11, 0))
        date5 = make_aware(datetime(2021, 6, 9, 3, 0))
        dates = [date1, date2, date3, date4, date5]
        results = []
        for date in dates:
            x, y = last_date(date)
            results.append((x,y))
        self.assertEqual(results, [((date1 - timedelta(days=1)).date(),True),((date2 - timedelta(days=2)).date(),True),
            (date3.date(),True),(date4.date(),False),((date5 - timedelta(days=1)).date(),True)])

    def test_growth_template_tag(self):
        """Test that the growth template tag returns the correct response"""
        randnumbs = [(random.random(),random.random()) for x in range(20)]
        outputs = [growth(x[0],x[1]) for x in randnumbs]
        doMath = [str(round(((x[1]-x[0])/x[0])*100,2))+"%" for x in randnumbs]
        self.assertEqual(outputs,doMath)

    def test_get_stock_info(self):
        """Tests that the get_stock_info function properly modifieds database with results"""
        s1 = Stock.objects.create(ticker="TSLA")
        s2 = Stock.objects.create(ticker="IWV")
        s3 = Stock.objects.create(ticker="Zewff")
        stocks = [s1, s2, s3]
        x = last_date(timezone.now())
        for stock in stocks:
            get_stock_info(stock)
        for stock in Stock.objects.all():
            if stock.active:
                self.assertTrue(stock.price > 0)
                self.assertTrue(stock.volume > 0)
                self.assertEqual(stock.last_updated.date(),x[0])
            else:
                self.assertEqual(stock.price, None)
                self.assertEqual(stock.volume, None)
                self.assertEqual(stock.last_updated, None)