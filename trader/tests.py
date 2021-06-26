from .functions import today_trade, valid_ticker, get_closing, daily_email, last_date
from django.utils.timezone import make_aware
from rest_framework.test import APITestCase
from .models import Decision, Stock
from rest_framework import status
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from datetime import timedelta
from datetime import datetime
from bs4 import BeautifulSoup

from datetime import time
import requests

tickers = ["TSLA", "AAPL", "AMZN", "GME", "F"]

# Create your tests here.
class AlgoTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(AlgoTestCase, cls).setUpClass()
        for ticker in tickers:
            Stock.objects.create(ticker=ticker)
        today_trade()
        cls.pick = Decision.objects.get()

    def test_possible_ticker(self):
        """Tests that the ticker chosen is a possible choice"""
        self.assertIn(self.pick.stock.ticker, tickers)

    def test_no_closing_price(self):
        """Tests that the stock getter does not set a closing price"""
        self.assertIsNone(self.pick.closingPrice)

    def test_correct_open_price(self):
        """Tests that the open price matches Yahoo's open price"""
        name = self.pick.stock.ticker
        URL = 'https://finance.yahoo.com/quote/'+name
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find(attrs={"data-reactid": "103"})
        yahooOpen = float(item.text)
        self.assertEqual(round(self.pick.openPrice,2), round(yahooOpen,2))


class ClosingTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ClosingTestCase, cls).setUpClass()
        for ticker in tickers:
            Stock.objects.create(ticker=ticker)
        today_trade()
        get_closing()
        cls.pick = Decision.objects.get()

    def test_proper_closing_entry(self):
        """Test that get_closing enters a possible closing price, or none if market is open"""
        weekday = timezone.now().weekday()
        currTime = timezone.now().time()
            
        if weekday < 5 and currTime > time(9,30,0) and currTime < time(16,0,0):
            self.assertIsNone(self.pick.closingPrice)
        else:
            self.assertTrue(self.pick.closingPrice > 0)

    def test_proper_closing_price(self):
        """Test that closing price matches Yahoo's closing price if market is closed"""



class EmailTestCase(TestCase):

    def test_email_sendgrid(self):
        """Checks that send_email works with Sendgrid properly"""

    def test_email_table_logic(self):
        """Animals that can speak are correctly identified"""



class HelpersTestCase(TestCase):

    def test_view_home(self):
        """Tests that home provides a basic repsonse"""
        response = self.client.get('', follow=True)
        self.assertTrue("This is the base URL for the daytrading API" in response.content.decode("utf-8") )

    def test_function_valid_ticker(self):
        """Test that the ticker function properly classifies strings"""
        self.tickers = ["AAPL","TSLA","XYZZY","ZZZ","IWV","AMZN","NARP","WEEN"]
        truthVals = [valid_ticker(x) for x in self.tickers]
        self.assertEqual(truthVals, [True,True,False,False,True,True,False,False])

    def test__view_get_cashflows(self):
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
        self.assertEqual(results, [((date1 - timedelta(days=1)).date(),True),((date2 - timedelta(days=2)).date(),True),(date3,True),(date4,False),((date5 - timedelta(days=1)).date(),True)])


class APITests(APITestCase):

    def test_API_stocks_get(self):
        """Test that the stocks API works with GET requests"""
        Stock.objects.create(ticker="T")
        Stock.objects.create(ticker="CANO")
        url = reverse('stocks-list')
        response = self.client.get(url)
        tickers = [x['ticker'] for x in response.json()]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('T' in tickers and 'CANO' in tickers)

    def test_API_stocks_post(self):
        """Test that the stocks API works with POST requests"""
        url = reverse('stocks-list')
        self.tickers = ["AAPL","TSLA","XYZZY","ZZZ","IWV","AMZN","NARP","WEEN","AAPL",""] 
        responses = [self.client.post(url, {'ticker': x}, format='json').status_code for x in self.tickers]
        h201 = status.HTTP_201_CREATED
        h400 = status.HTTP_400_BAD_REQUEST
        h406 = status.HTTP_406_NOT_ACCEPTABLE
        self.assertEqual(responses, [h201,h201,h406,h406,h201,h201,h406,h406,h400,h406])
        self.assertEqual(Stock.objects.count(), 4)

    
