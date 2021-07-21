from trader.functions.helpers import last_date, get_stock_data, get_highest_lowest, get_opening, get_closing, get_data, get_stock
from trader.functions.scrapers import valid_ticker, get_highest_performing, get_lowest_performing
from trader.models import Stock, Decision, Algorithm
from trader.templatetags.filter import growth
from django.utils.timezone import make_aware
from django.test import TransactionTestCase
from datetime import datetime, timedelta
from django.utils import timezone
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
            x, y, z = last_date(date)
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
        self.assertTrue(Stock.objects.get(ticker="F").price is None)
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
        self.assertTrue(Stock.objects.get(ticker="IWV").price is None)

    def test_get_stock_data_correct_order(self):
        """Tests that the functions gets stock data when called, and gets the last stocks to be updated first"""
        Stock.objects.create(ticker="T", listed=True)
        Stock.objects.create(ticker="NIO", last_updated=timezone.now() - timedelta(days=18),listed=True)
        Stock.objects.create(ticker="IWV", last_updated=timezone.now() - timedelta(days=15),listed=True)
        Stock.objects.create(ticker="AAPL", last_updated=timezone.now() - timedelta(days=12),listed=True)
        get_stock_data(Stock.objects.all(),2)
        self.assertTrue(Stock.objects.get(ticker="T").price > 0)
        self.assertTrue(Stock.objects.get(ticker="NIO").price > 0)
        self.assertTrue(Stock.objects.get(ticker="AAPL").price is None)
        self.assertTrue(Stock.objects.get(ticker="IWV").price is None)

    def test_get_stock_data_doesnt_run_listed_false(self):
        """Tests that the get_stock_data does not run stocks with a False listed attribute"""
        Stock.objects.create(ticker="NIO", last_updated=timezone.now() - timedelta(days=18),listed=True)
        Stock.objects.create(ticker="IWV", last_updated=timezone.now() - timedelta(days=15),listed=True)
        Stock.objects.create(ticker="T", listed=False)
        get_stock_data(Stock.objects.all(),3)
        self.assertTrue(Stock.objects.get(ticker="T").price is None)
        self.assertTrue(Stock.objects.get(ticker="IWV").price > 0)
        self.assertTrue(Stock.objects.get(ticker="NIO").price > 0)

    def test_get_highest_performing(self):
        highest = get_highest_performing()
        self.assertTrue(isinstance(highest, str))
        self.assertTrue(len(highest) > 0)
        self.assertTrue(len(highest) < 6)

    def test_get_lowest_performing(self):
        lowest = get_lowest_performing()
        self.assertTrue(isinstance(lowest, str))
        self.assertTrue(len(lowest) > 0)
        self.assertTrue(len(lowest) < 6)

    def test_get_highest_lowest(self):
        get_highest_lowest()
        algo1 = Algorithm.objects.get(name="Buy previous day's biggest gainer")
        algo2 = Algorithm.objects.get(name="Buy previous day's biggest loser")
        self.assertEqual(Decision.objects.filter(algorithm=algo1).count(),1)
        self.assertEqual(Decision.objects.filter(algorithm=algo2).count(),1)

    def test_get_highest_lowest_only_one(self):
        get_highest_lowest()
        get_highest_lowest()
        algo1 = Algorithm.objects.get(name="Buy previous day's biggest gainer")
        algo2 = Algorithm.objects.get(name="Buy previous day's biggest loser")
        self.assertEqual(Decision.objects.filter(algorithm=algo1).count(),1)
        self.assertEqual(Decision.objects.filter(algorithm=algo2).count(),1)

    def test_get_open_price(self):
        stock = Stock.objects.create(ticker="T", listed=True)
        algo = Algorithm.objects.create(name="Buy previous day's biggest gainer")
        Decision.objects.create(stock=stock, algorithm=algo, trade_date=make_aware(datetime(2021, 7, 7, 12, 0)), long=True)
        get_opening()
        self.assertTrue(Decision.objects.get(stock=stock).open_price > 0)

    def test_get_open_price_skips_weekend(self):
        stock = Stock.objects.create(ticker="T", listed=True)
        algo = Algorithm.objects.create(name="Buy previous day's biggest gainer")
        Decision.objects.create(stock=stock, algorithm=algo, trade_date=make_aware(datetime(2021, 7, 18, 12, 0)), long=True)
        get_opening()
        self.assertTrue(Decision.objects.get(stock=stock).open_price is None)

    def test_get_close_price(self):
        stock = Stock.objects.create(ticker="T", listed=True)
        algo = Algorithm.objects.create(name="Buy previous day's biggest gainer")
        Decision.objects.create(stock=stock, algorithm=algo, trade_date=make_aware(datetime(2021, 7, 7, 12, 0)), long=True)
        get_closing()
        self.assertTrue(Decision.objects.get(stock=stock).closing_price > 0)

    def test_get_close_price_skips_weekend(self):
        stock = Stock.objects.create(ticker="T", listed=True)
        algo = Algorithm.objects.create(name="Buy previous day's biggest gainer")
        Decision.objects.create(stock=stock, algorithm=algo, trade_date=make_aware(datetime(2021, 7, 18, 12, 0)), long=True)
        get_closing()
        self.assertTrue(Decision.objects.get(stock=stock).closing_price is None)

    def test_last_date_never_returns_weekend(self):
        days = [make_aware(datetime(2021, 7, x, 12, 0)) for x in [1,2,3,4,5,6,7,8,9,10]]
        values = [last_date(x) for x in days]
        last_date_values = [x[0].weekday() for x in values]
        next_date_values = [x[2].weekday() for x in values]
        self.assertFalse(5 in last_date_values or 6 in last_date_values)
        self.assertFalse(5 in next_date_values or 6 in next_date_values)

    def test_get_data_filters_null(self):
        symbols = ["AAPL","RKDA","TSLA","GXGX"]
        data = get_data(symbols)
        columns = set([x[1] for x in data.columns])
        print(columns)
        self.assertTrue("AAPL" in columns and "RKDA" in columns and "TSLA" in columns)
        self.assertFalse("GXGX" in columns)

    def test_get_stock_wont_enter_if_bad_data(self):
        stock = Stock.objects.create(name="GXGX")
        algo = Algorithm.objects.create(name="Test algo")
        get_stock(algo, [stock])
        self.assertEqual(Decision.objects.all().count(),0)