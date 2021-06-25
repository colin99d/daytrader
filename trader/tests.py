from .functions import today_trade, valid_ticker, get_closing, get_cashflows, daily_email
from .models import Decision, Stock
from django.utils import timezone
from django.test import TestCase
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

    def test_proper_closing_price(self):
        """Test that get_closing enters a possible closing price, or none if market is open"""
        weekday = timezone.now().weekday()
        currTime = timezone.now().time()
            
        if weekday < 5 and currTime > time(9,30,0) and currTime < time(16,0,0):
            self.assertIsNone(self.pick.closingPrice)
        else:
            self.assertTrue(self.pick.closingPrice > 0)



"""
class EmailTestCase(TestCase):
    def setUp(self):
        pass

    def test_animals_can_speak(self):
        Animals that can speak are correctly identified
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
"""


class HelpersTestCase(TestCase):

    def test_function_valid_ticker(self):
        """Test that the ticker function properly classifies strings"""
        self.tickers = ["AAPL","TSLA","XYZZY","ZZZ","IWV","AMZN","NARP","WEEN"]
        truthVals = [valid_ticker(x) for x in self.tickers]
        self.assertEqual(truthVals, [True,True,False,False,True,True,False,False])

    def test_view_valid_ticker(self):
        """Tests that the ticker view sends the correct response"""

