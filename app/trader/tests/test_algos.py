from trader.functions.helpers import get_closing, get_stock
from trader.models import Stock, Algorithm, Decision
from django.test import TransactionTestCase
from django.utils import timezone
from datetime import time, date
from bs4 import BeautifulSoup
import requests

tickers = ["TSLA", "AAPL", "AMZN", "GME", "F"]

# Create your tests here.
class AlgoTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(AlgoTestCase, cls).setUpClass()
        for ticker in tickers:
            Stock.objects.create(ticker=ticker)
        algo = Algorithm.objects.create(name="The test algo",public=True)
        get_stock(algo, Stock.objects.all())
        cls.pick = Decision.objects.get()

    def test_possible_ticker(self):
        """Tests that the ticker chosen is a possible choice"""
        self.assertIn(self.pick.stock.ticker, tickers)

    def test_no_closing_price(self):
        """Tests that the stock getter does not set a closing price"""
        self.assertIsNone(self.pick.closing_price)

    def test_correct_open_price(self):
        """Tests that the open price matches Yahoo's open price"""
        name = self.pick.stock.ticker
        URL = 'https://finance.yahoo.com/quote/'+name
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find(attrs={"data-test": "OPEN-value"})
        item = item.find("span")
        yahooOpen = float(item.text)
        self.assertEqual(round(self.pick.open_price,2), round(yahooOpen,2))

    def test_no_second_pick(self):
        """Tests that the get_stock function blocks two stock picks in one day"""
        for ticker in tickers:
            Stock.objects.create(ticker=ticker)
        algo = Algorithm.objects.create(name="The test algo",public=True)
        get_stock(algo, Stock.objects.all())
        self.assertEqual(Decision.objects.count(),1)
        get_stock(algo, Stock.objects.all())
        self.assertEqual(Decision.objects.count(),1)

class ClosingTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(ClosingTestCase, cls).setUpClass()
        for ticker in tickers:
            Stock.objects.get_or_create(ticker=ticker)
        algo = Algorithm.objects.create(name="The test algo",public=True)
        get_stock(algo, Stock.objects.all().order_by('-volume'))
        get_closing()
        cls.pick = Decision.objects.get()

    def test_proper_closing_entry(self):
        """Test that get_closing enters a possible closing price, or none if market is open"""
        weekday = timezone.now().weekday()
        currTime = timezone.now().time()

        holidays = [date(2021,7,5),date(2021,9,6),date(2021,12,24),date(2022,1,17),date(2022,2,21),date(2022,4,15),date(2022,5,30),date(2022,7,4),
                    date(2022,9,5),date(2022,12,26),date(2023,1,2),date(2023,1,16),date(2023,2,20),date(2023,4,7),date(2023,5,29),date(2023,7,4),
                    date(2023,9,4),date(2023,12,25)]
        
        if weekday < 5 and currTime > time(9,30,0) and currTime < time(16,0,0) and timezone.now().date not in holidays:
            self.assertIsNone(self.pick.closing_price)
        else:
            self.assertTrue(self.pick.closing_price > 0)

    def test_proper_closing_price(self):
        """Test that closing price matches Yahoo's closing price if market is closed"""
