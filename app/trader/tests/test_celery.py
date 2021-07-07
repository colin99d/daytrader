from daytrader.celery import begin_day, end_day, send_email, get_stock_tickers
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
        """Test that the begin_day celery function adds a decision to the model and sends an email to the user"""
        User.objects.create_user('testUser','test@gmail.com','secure49password')
        for ticker in tickers:
            Stock.objects.create(ticker=ticker)
        decisions = begin_day.apply().get()
        self.assertEqual(len(decisions),1)
        self.assertTrue(decisions[0].openPrice > 0)
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_end_day(self):
        """Test that the end_day celery function adds a closing price to all decisions without one"""
        s1 = Stock.objects.create(ticker="IWV")
        s2 = Stock.objects.create(ticker="TSLA")
        s3 = Stock.objects.create(ticker="AMC")
        a = Algorithm.objects.create(name="Basic algo", public=True)
        Decision.objects.create(stock=s1,algorithm=a,openPrice=23.22,confidence=32.87,tradeDate=make_aware(datetime(2017, 10, 27, 12, 0)).date())
        Decision.objects.create(stock=s2,algorithm=a,openPrice=23.22,confidence=32.87,tradeDate=make_aware(datetime(2018, 6, 8, 12, 0)).date())
        Decision.objects.create(stock=s3,algorithm=a,openPrice=23.22,confidence=32.87,tradeDate=make_aware(datetime(2019, 12, 27, 12, 0)).date())
        decisions = end_day.apply().get()
        closings = [x.closingPrice for x in decisions]
        for closing in closings:
            self.assertTrue(closing > 0)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_email(self):
        """Test that the send_email celery function sends an email to the user"""
        User.objects.create_user('testUser','test@gmail.com','secure49password')
        send_email.apply().get()
        self.assertEqual(len(mail.outbox), 1)

    def test_task(self):
        self.assertEqual(begin_day.run().count(),0)
        self.assertEqual(end_day.run().count(),0)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_get_tickers(self):
        items = get_stock_tickers()
        self.assertTrue(items.filter(exchange="NYSE").count() > 500)
        self.assertTrue(items.filter(exchange="NASDAQ").count() > 500)
