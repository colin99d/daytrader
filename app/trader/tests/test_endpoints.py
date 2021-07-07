from trader.views import StockView, AlgorithmView, DecisionView
from trader.models import Algorithm, Decision, Stock
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.utils import timezone
from rest_framework import status
from django.urls import reverse
from user.models import User
import json


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

    def test_API_stock_get(self):
        """Test that the stock API works with GET requests"""
        Stock.objects.create(ticker="T")
        Stock.objects.create(ticker="CANO")
        url = reverse('stocks-list')
        response = self.make_request("GET",url, StockView)
        tickers = [x['ticker'] for x in json.loads(response.content)]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('T' in tickers and 'CANO' in tickers)

    def test_API_stock_post(self):
        """Test that the stock API works with POST requests"""
        url = reverse('stocks-list')
        self.tickers = ["AAPL","TSLA","XYZZY","ZZZ","IWV","AMZN","NARP","WEEN","AAPL",""] 
        responses = [self.make_request("POST",url, StockView, {'ticker': x}).status_code for x in self.tickers]
        h201 = status.HTTP_201_CREATED
        h400 = status.HTTP_400_BAD_REQUEST
        h406 = status.HTTP_406_NOT_ACCEPTABLE
        self.assertEqual(responses, [h201,h201,h406,h406,h201,h201,h406,h406,h400,h400])
        self.assertEqual(Stock.objects.count(), 4)

    def test_API_algorithm_get(self):
        """Test that the algorithm API works with GET requests"""
        Algorithm.objects.create(name="Buy low sell high2", public=True)
        Algorithm.objects.create(name="Buy high sell low2", public=False)
        url = reverse('algorithms-list')
        response = self.make_request("GET",url, AlgorithmView)
        names = [x['name'] for x in json.loads(response.content)]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("Buy low sell high2" in names and "Buy high sell low2" in names)

    def test_API_algorithm_post(self):
        """Test that the algorithm API works with POST requests"""
        url = reverse('stocks-list')
        names = [("This is a new algorithm",True),("",False)] 
        responses = [self.make_request("POST",url, AlgorithmView, {'name':x[0], 'public':x[1]}).status_code for x in names]
        h201 = status.HTTP_201_CREATED
        h400 = status.HTTP_400_BAD_REQUEST
        self.assertEqual(responses, [h201,h400])
        self.assertEqual(Algorithm.objects.count(), 1)

    def test_API_decision_get(self):
        """Test that the decision API works with GET requests"""
        s1 = Stock.objects.create(ticker="CANO")
        s2 = Stock.objects.create(ticker="CMAX")
        a1 = Algorithm.objects.create(name="Buy low sell high", public=True)
        a2 = Algorithm.objects.create(name="Buy high sell low", public=False)
        Decision.objects.create(stock=s1, algorithm=a1, openPrice=27.25, confidence=87.32, tradeDate=timezone.now().date())
        Decision.objects.create(stock=s2, algorithm=a2, openPrice=13.38, confidence=22.45, tradeDate=timezone.now().date())
        url = reverse('decisions-list')
        response = self.make_request("GET",url, DecisionView)
        names = [x['stock']['ticker'] for x in json.loads(response.content)]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("CANO" in names and "CMAX" in names)

    def test_API_decision_post(self):
        """Test that the decision API works with POST requests"""
        s1 = Stock.objects.create(ticker="CANO")
        s2 = Stock.objects.create(ticker="CMAX")
        a1 = Algorithm.objects.create(name="Buy low sell high", public=True)
        a2 = Algorithm.objects.create(name="Buy high sell low", public=False)
        url = reverse('decisions-list')
        decisions = [{"stock": s1.id, "algorithm":a1.id,"openPrice":13.24,"confidence":36.89,"tradeDate":timezone.now().date()},
            {"stock": s2.id, "algorithm":a2.id,"openPrice":22.24,"confidence":0,"tradeDate":timezone.now().date()}, {}] 
        responses = [self.make_request("POST",url, DecisionView, x).status_code for x in decisions]
        h201 = status.HTTP_201_CREATED
        h400 = status.HTTP_400_BAD_REQUEST
        self.assertEqual(responses, [h201,h201,h400])
        self.assertEqual(Decision.objects.count(), 2)