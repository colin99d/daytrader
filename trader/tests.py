from .functions import today_trade, valid_ticker, get_closing, daily_email, last_date
from daytrader.celery import begin_day, end_day, send_email
from .models import Algorithm, Decision, Stock
from django.utils.timezone import make_aware
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .templatetags.filter import growth
from rest_framework import status
from django.utils import timezone
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from datetime import timedelta
from datetime import datetime
from bs4 import BeautifulSoup
import requests, random, json
from django.core import mail
from datetime import time

from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from .views import StockView


tickers = ["TSLA", "AAPL", "AMZN", "GME", "F"]

# Create your tests here.
class AlgoTestCase(TransactionTestCase):
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


class ClosingTestCase(TransactionTestCase):

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


class EmailTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(EmailTestCase, cls).setUpClass()
        cls.user = User.objects.create_user('testUser','test@gmail.com','secure49password')

    def test_email_sendgrid(self):
        """Checks that send_email properly sends an email"""
        daily_email(self.user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test@gmail.com'])
        self.assertEqual(mail.outbox[0].from_email, 'cdelahun@iu.edu')
        self.assertEqual(mail.outbox[0].subject, 'Daily Stock Pick')

    def test_email_table_logic(self):
        """Animals that can speak are correctly identified"""


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
        self.assertEqual(results, [((date1 - timedelta(days=1)).date(),True),((date2 - timedelta(days=2)).date(),True),(date3.date(),True),(date4.date(),False),((date5 - timedelta(days=1)).date(),True)])

    def test_growth_template_tag(self):
        """Test that the growth template tag returns the correct response"""
        randnumbs = [(random.random(),random.random()) for x in range(20)]
        outputs = [growth(x[0],x[1]) for x in randnumbs]
        doMath = [str(round(((x[1]-x[0])/x[0])*100,2))+"%" for x in randnumbs]
        self.assertEqual(outputs,doMath)
        

class APITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('test1','test@email.com', 'qwe123qwe')

    def make_request(self, method,  url, serView, data=None):
        factory = APIRequestFactory()
        view = serView.as_view({'post': 'create', 'get': 'list'})
        if method == "GET":
            request = factory.get(url, format='json')
        elif method == "POST":
            request = factory.post(url,data, format='json')
        
        force_authenticate(request, user=self.user)
        return view(request).render()

    def test_API_stocks_get(self):
        """Test that the stocks API works with GET requests"""
        Stock.objects.create(ticker="T")
        Stock.objects.create(ticker="CANO")
        url = reverse('stocks-list')
        response = self.make_request("GET",url, StockView)
        print(json.loads(response.content))
        tickers = [x['ticker'] for x in json.loads(response.content)]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('T' in tickers and 'CANO' in tickers)

    def test_API_stocks_post(self):
        """Test that the stocks API works with POST requests"""
        url = reverse('stocks-list')
        self.tickers = ["AAPL","TSLA","XYZZY","ZZZ","IWV","AMZN","NARP","WEEN","AAPL",""] 
        responses = [self.make_request("POST",url, StockView, {'ticker': x}).status_code for x in self.tickers]
        h201 = status.HTTP_201_CREATED
        h400 = status.HTTP_400_BAD_REQUEST
        h406 = status.HTTP_406_NOT_ACCEPTABLE
        self.assertEqual(responses, [h201,h201,h406,h406,h201,h201,h406,h406,h400,h400])
        self.assertEqual(Stock.objects.count(), 4)

class ModelMethodTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ModelMethodTestCase, cls).setUpClass()
        cls.ticker = "AAPL"
        cls.stock = Stock.objects.create(ticker=cls.ticker)
        cls.algoName = "A bitcoin daytrading algorithm"
        cls.algo = Algorithm.objects.create(name=cls.algoName, public=True)

    def test_stock_str(self):
        """Test that the stock str method returns the ticker"""
        self.assertEqual(self.ticker,self.stock.__str__())

    def test_algo_str(self):
        """Test that the algorithm str method returns the ticker"""
        self.assertEqual(self.algoName,self.algo.__str__())

    def test_decision_str(self):
        """Test that the decision str method returns the ticker"""
        self.tradeDate = timezone.now().date()
        self.decision = Decision.objects.create(stock=self.stock,algorithm=self.algo,openPrice=10,confidence=.2,tradeDate=self.tradeDate)
        self.assertEqual(str(self.stock) + ' on ' + str(self.tradeDate), self.decision.__str__())

    
