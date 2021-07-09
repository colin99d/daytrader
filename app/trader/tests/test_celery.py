from daytrader.celery import begin_day, end_day, get_stock_tickers, get_stock_info
from trader.models import Algorithm, Decision, Stock
from django.test.utils import override_settings
from django.utils.timezone import make_aware
from django.test import TestCase
from datetime import datetime
from user.models import User
from django.core import mail

tickers = ["TSLA", "AAPL", "AMZN", "GME", "F"]

class CeleryFeaturesTestCase(TestCase):

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_begin_day(self):
        """Test that the begin_day celery function adds a decision to the model and sends an email to the user and chooses highest volume"""
        User.objects.create_user('testUser','test@gmail.com','secure49password')
        s1 = Stock.objects.create(ticker = "TSLA", volume=10000,price=0,listed=True)
        s2 = Stock.objects.create(ticker = "AAPL", volume=2000,price=1000,listed=True)
        s3 = Stock.objects.create(ticker = "AMZN", volume=3000,price=83,listed=True)
        s4 = Stock.objects.create(ticker = "GME", volume=4000,price=51,listed=True)
        s5 = Stock.objects.create(ticker = "F", volume=5000,price=26,listed=True)
        s6 = Stock.objects.create(ticker = "T", volume=6000,price=132,listed=True)
        s7 = Stock.objects.create(ticker = "CANO", volume=7000,price=56,listed=True)
        s8 = Stock.objects.create(ticker = "CMAX", volume=8000,price=200,listed=True)
        s9 = Stock.objects.create(ticker = "IWV", volume=20000,price=10,listed=False)
        decisions = begin_day(2)
        self.assertEqual(len(decisions),1)
        self.assertTrue(decisions[0].openPrice > 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(decisions[0].stock == s7 or decisions[0].stock == s5)


    def test_begin_day_lots_more(self):
        """Test that the begin_day celery function adds a decision to the model and sends an email to the user and doesn't choose a price over 100"""
        User.objects.create_user('testUser','test@gmail.com','secure49password')
        s1 = Stock.objects.create(ticker = "TSLA", volume=1000,price=20,listed=True)
        s2 = Stock.objects.create(ticker = "AAPL", volume=2000,price=1000,listed=True)
        s3 = Stock.objects.create(ticker = "AMZN", volume=3000,price=83,listed=True)
        s4 = Stock.objects.create(ticker = "GME", volume=4000,price=51,listed=True)
        s5 = Stock.objects.create(ticker = "F", volume=5000,price=26,listed=True)
        s6 = Stock.objects.create(ticker = "T", volume=6000,price=132,listed=True)
        s7 = Stock.objects.create(ticker = "CANO", volume=7000,price=56,listed=True)
        s8 = Stock.objects.create(ticker = "CMAX", volume=8000,price=200,listed=True)
        s9 = Stock.objects.create(ticker = "IWV", volume=20000,price=10,listed=False)
        decisions = begin_day(5)
        self.assertEqual(len(decisions),1)
        self.assertTrue(decisions[0].openPrice > 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(decisions[0].stock not in [s8,s6,s2,s9])


    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_end_day(self):
        """Test that the end_day celery function adds a closing price to all decisions without one"""
        s1 = Stock.objects.create(ticker="IWV")
        s2 = Stock.objects.create(ticker="TSLA")
        s3 = Stock.objects.create(ticker="AMC")
        a = Algorithm.objects.create(name="Basic algo", public=True)
        Decision.objects.create(stock=s1,algorithm=a,openPrice=23.22,confidence=32.87,tradeDate=make_aware(datetime(2017, 10, 27, 12, 0)).date(), long=True)
        Decision.objects.create(stock=s2,algorithm=a,openPrice=23.22,confidence=32.87,tradeDate=make_aware(datetime(2018, 6, 8, 12, 0)).date(), long=True)
        Decision.objects.create(stock=s3,algorithm=a,openPrice=23.22,confidence=32.87,tradeDate=make_aware(datetime(2019, 12, 27, 12, 0)).date(), long=True)
        decisions = end_day.apply().get()
        closings = [x.closingPrice for x in decisions]
        for closing in closings:
            self.assertTrue(closing > 0)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_get_tickers(self):
        items = get_stock_tickers()
        self.assertTrue(items.filter(exchange="NYSE").count() > 500)
        self.assertTrue(items.filter(exchange="NASDAQ").count() > 500)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_update_ticker_information(self):
        for ticker in tickers:
            Stock.objects.create(ticker=ticker)
        get_stock_info(4)
        self.assertEqual(Stock.objects.filter(price__gt=0).count(),4)
