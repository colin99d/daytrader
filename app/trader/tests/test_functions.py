from trader.functions.helpers import last_date, get_stock_data
from trader.functions.scrapers import valid_ticker
from trader.templatetags.filter import growth
from django.utils.timezone import make_aware
from django.test import TransactionTestCase
from datetime import datetime, timedelta
from django.utils import timezone
from trader.models import Stock
import random

class HelpersTestCase(TransactionTestCase):

    def test_function_valid_ticker(self):
        """Test that the ticker function properly classifies strings"""
        self.tickers = ["AAPL","TSLA","XYZZY","ZZZ","IWV","AMZN","NARP","WEEN"]
        truthVals = [valid_ticker(x) for x in self.tickers]
        self.assertEqual(truthVals, [True,True,False,False,True,True,False,False])

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

    def test_get_stock_data(self):
        """Tests that the functions gets stock data when called, if it has been more than 6 days since the last attempt"""
        Stock.objects.create(ticker="NIO", last_updated=timezone.now() - timedelta(days=18),listed=True)
        Stock.objects.create(ticker="IWV", last_updated=timezone.now() - timedelta(days=15),listed=True)
        Stock.objects.create(ticker="F", last_updated=timezone.now() - timedelta(days=4),listed=True)
        get_stock_data(Stock.objects.all(),3)
        self.assertEqual(Stock.objects.filter(price__gt=0).count(),2)
        self.assertTrue(Stock.objects.get(ticker="NIO").price > 0)
        self.assertTrue(Stock.objects.get(ticker="IWV").price > 0)
        self.assertTrue(Stock.objects.get(ticker="F").price == None)
        get_stock_data(Stock.objects.all(),3)
        self.assertEqual(Stock.objects.filter(price__gt=0).count(),2)

    def test_get_stock_data_delisted(self):
        """Tests that the function understands if a stock is delisted and changes model"""
        Stock.objects.create(ticker="SSS",listed=True)
        get_stock_data(Stock.objects.all(),1)
        self.assertFalse(Stock.objects.get(ticker="SSS").listed)

    def test_get_stock_data_skips_delisted(self):
        """Tests that the functions gets stock data when called, it skips delisted stocks"""
        Stock.objects.create(ticker="NIO", last_updated=timezone.now() - timedelta(days=18),listed=True)
        Stock.objects.create(ticker="IWV", last_updated=timezone.now() - timedelta(days=15),listed=False)
        get_stock_data(Stock.objects.all(),2)
        self.assertTrue(Stock.objects.get(ticker="NIO").price > 0)
        self.assertTrue(Stock.objects.get(ticker="IWV").price == None)

    def test_get_stock_data_correct_order(self):
        """Tests that the functions gets stock data when called, and gets the last stocks to be updated first"""
        Stock.objects.create(ticker="T", listed=True)
        Stock.objects.create(ticker="NIO", last_updated=timezone.now() - timedelta(days=18),listed=True)
        Stock.objects.create(ticker="IWV", last_updated=timezone.now() - timedelta(days=15),listed=True)
        Stock.objects.create(ticker="AAPL", last_updated=timezone.now() - timedelta(days=12),listed=True)
        get_stock_data(Stock.objects.all(),2)
        self.assertTrue(Stock.objects.get(ticker="T").price > 0)
        self.assertTrue(Stock.objects.get(ticker="NIO").price > 0)
        self.assertTrue(Stock.objects.get(ticker="AAPL").price == None)
        self.assertTrue(Stock.objects.get(ticker="IWV").price == None)

    def test_get_stock_data_doesnt_run_listed_false(self):
        """Tests that the get_stock_data does not run stocks with a False listed attribute"""
        Stock.objects.create(ticker="NIO", last_updated=timezone.now() - timedelta(days=18),listed=True)
        Stock.objects.create(ticker="IWV", last_updated=timezone.now() - timedelta(days=15),listed=True)
        Stock.objects.create(ticker="T", listed=False)
        get_stock_data(Stock.objects.all(),3)
        self.assertTrue(Stock.objects.get(ticker="T").price == None)
        self.assertTrue(Stock.objects.get(ticker="IWV").price > 0)
        self.assertTrue(Stock.objects.get(ticker="NIO").price > 0)