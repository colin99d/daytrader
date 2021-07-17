from daytrader.celery import begin_day, end_day, get_stock_tickers, get_stock_info, get_high_and_low, send_email
from trader.models import Algorithm, Decision, Stock
from django.test.utils import override_settings
from django.utils.timezone import make_aware
from django.test import TestCase
from datetime import datetime
from user.models import User
from django.core import mail
import json

tickers = ["TSLA", "AAPL", "AMZN", "GME", "F"]

class CeleryFeaturesTestCase(TestCase):

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_begin_day(self):
        """Test that the begin_day celery function adds a decision to the model and sends an email to the user and chooses highest volume"""
        user = User.objects.create_user('testUser','test@gmail.com','secure49password')
        setattr(user,"daily_emails",True)
        setattr(user,"selected_algo",Algorithm.objects.create(name="Z-score daytrader",public=True))
        user.save()
        s1 = Stock.objects.create(ticker = "TSLA", volume=10000,price=0,listed=True)
        s2 = Stock.objects.create(ticker = "AAPL", volume=2000,price=1000,listed=True)
        s3 = Stock.objects.create(ticker = "AMZN", volume=3000,price=83,listed=True)
        s4 = Stock.objects.create(ticker = "GME", volume=4000,price=51,listed=True)
        s5 = Stock.objects.create(ticker = "F", volume=5000,price=26,listed=True)
        s6 = Stock.objects.create(ticker = "T", volume=6000,price=132,listed=True)
        s7 = Stock.objects.create(ticker = "CANO", volume=7000,price=56,listed=True)
        s8 = Stock.objects.create(ticker = "CMAX", volume=8000,price=200,listed=True)
        s9 = Stock.objects.create(ticker = "IWV", volume=20000,price=10,listed=False)
        decisions = begin_day.delay(2)
        decisions = json.loads(decisions.get())
        self.assertEqual(len(decisions),1)
        self.assertTrue(decisions[0]["fields"]["open_price"] > 0)
        self.assertEqual(len(mail.outbox), 1)
        stock = decisions[0]["fields"]["stock"]
        self.assertTrue(stock == s7.id or stock == s5.id)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_begin_day_lots_more(self):
        """Test that the begin_day celery function adds a decision to the model and sends an email to the user and doesn't choose a price over 100"""
        user = User.objects.create_user('testUser','test@gmail.com','secure49password')
        setattr(user,"daily_emails",True)
        setattr(user,"selected_algo",Algorithm.objects.create(name="Z-score daytrader",public=True))
        user.save()
        s1 = Stock.objects.create(ticker = "TSLA", volume=1000,price=20,listed=True)
        s2 = Stock.objects.create(ticker = "AAPL", volume=2000,price=1000,listed=True)
        s3 = Stock.objects.create(ticker = "AMZN", volume=3000,price=83,listed=True)
        s4 = Stock.objects.create(ticker = "GME", volume=4000,price=51,listed=True)
        s5 = Stock.objects.create(ticker = "F", volume=5000,price=26,listed=True)
        s6 = Stock.objects.create(ticker = "T", volume=6000,price=132,listed=True)
        s7 = Stock.objects.create(ticker = "CANO", volume=7000,price=56,listed=True)
        s8 = Stock.objects.create(ticker = "CMAX", volume=8000,price=200,listed=True)
        s9 = Stock.objects.create(ticker = "IWV", volume=20000,price=10,listed=False)
        decisions = begin_day.delay(5)
        decisions = json.loads(decisions.get())
        self.assertEqual(len(decisions),1)
        self.assertTrue(decisions[0]["fields"]["open_price"] > 0)
        self.assertEqual(len(mail.outbox), 1)
        stock = decisions[0]["fields"]["stock"]
        self.assertTrue(stock not in [x.id for x in [s8,s6,s2,s9]])


    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_end_day(self):
        """Test that the end_day celery function adds a closing price to all decisions without one"""
        s1 = Stock.objects.create(ticker="IWV")
        s2 = Stock.objects.create(ticker="TSLA")
        s3 = Stock.objects.create(ticker="AMC")
        a = Algorithm.objects.create(name="Basic algo", public=True)
        Decision.objects.create(stock=s1,algorithm=a,open_price=23.22,confidence=32.87,trade_date=make_aware(datetime(2017, 10, 27, 12, 0)).date(), long=True)
        Decision.objects.create(stock=s2,algorithm=a,open_price=23.22,confidence=32.87,trade_date=make_aware(datetime(2018, 6, 8, 12, 0)).date(), long=True)
        Decision.objects.create(stock=s3,algorithm=a,open_price=23.22,confidence=32.87,trade_date=make_aware(datetime(2019, 12, 27, 12, 0)).date(), long=True)
        decisions = end_day.delay()
        decisions = json.loads(decisions.get())
        closings = [x["fields"]["closing_price"] for x in decisions]
        for closing in closings:
            self.assertTrue(closing > 0)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_get_tickers(self):
        items = get_stock_tickers.delay()
        items = json.loads(items.get())
        i = 0
        for item in items:
            i += 1
        self.assertTrue(i > 1000)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_update_ticker_information(self):
        for ticker in tickers:
            Stock.objects.create(ticker=ticker)
        get_stock_info.delay(4)
        self.assertEqual(Stock.objects.filter(price__gt=0).count(),4)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_update_ticker_information_delists_properly(self):
        Stock.objects.create(ticker="AEGN")
        Stock.objects.create(ticker="APXTU")
        items = get_stock_info.delay(2)
        items = json.loads(items.get())
        for item in items:
            self.assertTrue(item["fields"]["active"] == False)
            self.assertTrue(item["fields"]["listed"] == False)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_get_high_and_low(self):
        items = get_high_and_low.delay()
        items = json.loads(items.get())
        stocks = [x["fields"]["stock"] for x in items]
        for item in stocks:
            self.assertTrue(item > 0)

    
    def test_begin_day_gets_open_price(self):
        stock = Stock.objects.create(ticker="T", listed=True)
        for ticker in ["AAPL","GME","TSLA","CMAX","CANO"]:
            Stock.objects.create(ticker=ticker, listed=True)
        algo = Algorithm.objects.create(name="Buy previous day's biggest gainer")
        Decision.objects.create(stock=stock, algorithm=algo, trade_date=make_aware(datetime(2021, 7, 6, 12, 0)), long=True)
        Decision.objects.create(stock=stock, algorithm=algo, trade_date=make_aware(datetime(2021, 7, 7, 12, 0)), long=True)
        Decision.objects.create(stock=stock, algorithm=algo, trade_date=make_aware(datetime(2021, 7, 8, 12, 0)), long=True)
        decisions = begin_day.delay(5)
        decisions = json.loads(decisions.get())
        for decision in decisions:
            self.assertTrue(decision['fields']['open_price'] > 0)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_email_only_sends_on_matching_algo(self):
        """Tests that users only receive an email if they chose the selected algorithm"""
        algo1 = Algorithm.objects.create(name="Test the algo")
        algo2 = Algorithm.objects.create(name="Test this algo also")
        user = User.objects.create_user('testUser','test@gmail.com','secure49password')
        setattr(user,"selected_algo",algo1)
        setattr(user,"daily_emails",True)
        user.save()
        send_email.delay(algo2.pk)
        self.assertEqual(len(mail.outbox), 0)
        send_email.delay(algo1.pk)
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,CELERY_ALWAYS_EAGER=True,BROKER_BACKEND='memory')
    def test_email_only_sends_to_daily_emails_true(self):
        """Tests that users only receive an email if they chose to receive emails"""
        algo1 = Algorithm.objects.create(name="Test the algo")
        user1 = User.objects.create_user('testUser','test@gmail.com','secure49password')
        user2 = User.objects.create_user('testUser2','test2@gmail.com','secure249password')
        user3 = User.objects.create_user('testUser3','test3@gmail.com','secure349password')
        setattr(user1,"daily_emails",True)
        setattr(user1,"selected_algo",algo1)
        user1.save()
        setattr(user2,"daily_emails",False)
        setattr(user2,"selected_algo",algo1)
        user2.save()
        setattr(user3,"selected_algo",algo1)
        user3.save()
        send_email.delay(algo1.pk)
        self.assertEqual(len(mail.outbox), 1)
