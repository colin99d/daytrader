from trader.views import StockView, AlgorithmView, DecisionView
from trader.models import Algorithm, Decision, Stock
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from django.urls import reverse
from user.models import User
import json


class APITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('test1','test@email.com', 'qwe123qwe')
        setattr(self.user,"premium",True)
        self.user.save()

    def make_request(self, method,  url, serView, data=None, user=None):
        factory = APIRequestFactory()
        view = serView.as_view({'post': 'create', 'get': 'list'})
        if method == "GET":
            request = factory.get(url, format='json')
        elif method == "POST":
            request = factory.post(url,data, format='json')
        if user is None:
            force_authenticate(request, user=self.user)
        else:
            force_authenticate(request, user=user)
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

    def test_API_algorithm_get_non_premium(self):
        """Test that the algorithm API works with GET requests and filters out private algos"""
        Algorithm.objects.create(name="I am a public algo", public=True)
        Algorithm.objects.create(name="I am a private algo", public=False)
        url = reverse('algorithms-list')
        nonPrem = User.objects.create_user('test2','test2@email.com', 'qwe123qwe2')
        setattr(nonPrem,"premium",False)
        nonPrem.save()
        response = self.make_request("GET",url, AlgorithmView, user=nonPrem)
        names = [x['name'] for x in json.loads(response.content)]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("I am a public algo" in names and "I am a private algo" not in names)

    def test_API_algorithm_get_premium(self):
        """Test that the algorithm API works with GET requests"""
        Algorithm.objects.create(name="I am a public algo", public=True)
        Algorithm.objects.create(name="I am a private algo", public=False)
        url = reverse('algorithms-list')
        response = self.make_request("GET",url, AlgorithmView)
        names = [x['name'] for x in json.loads(response.content)]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("I am a public algo" in names and "I am a private algo" in names)

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
        Decision.objects.create(stock=s1, algorithm=a1, open_price=27.25, confidence=87.32, trade_date=timezone.now().date(), long=True)
        Decision.objects.create(stock=s2, algorithm=a2, open_price=13.38, confidence=22.45, trade_date=timezone.now().date(), long=True)
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
        decisions = [{"stock": s1.id, "algorithm":a1.id,"open_price":13.24,"confidence":36.89,"trade_date":timezone.now().date(),"long":True},
            {"stock": s2.id, "algorithm":a2.id,"open_price":22.24,"confidence":0,"trade_date":timezone.now().date(),"long":True}, {}] 
        responses = [self.make_request("POST",url, DecisionView, x).status_code for x in decisions]
        h201 = status.HTTP_201_CREATED
        h400 = status.HTTP_400_BAD_REQUEST
        self.assertEqual(responses, [h201,h201,h400])
        self.assertEqual(Decision.objects.count(), 2)

class ViewTests(TestCase):
    def test_view_home(self):
        """Tests that home provides a basic repsonse"""
        response = self.client.get('/backend/', follow=True)
        self.assertTrue("This is the base URL for the daytrading API" in response.content.decode("utf-8"))

    def test_view_get_cashflows(self):
        """Ensures that the get_cashflow function response returns json"""
        tickers = ["IWV","AAPL","TSLA","GME","ZZZZ"]
        for ticker in tickers[:4]:
            Stock.objects.create(ticker=ticker)
        responses = [self.client.post(reverse("cashflows"),{'ticker':x}, format="json") for x in tickers]
        h200 = status.HTTP_200_OK
        h406 = status.HTTP_406_NOT_ACCEPTABLE
        self.assertEqual([x.status_code for x in responses], [h200, h200, h200, h200, h406])
        self.assertIn("id", responses[1].json()["cashflows"][0].keys())

    def test_view_get_cashflows_update(self):
        """Ensures that the get_cashflow function response returns just cashflows if expiration"""
        s1 = Stock.objects.create(ticker="TSLA")
        response1 = s1.get_options_chain()
        expiration = response1["expirations"][4]
        response = self.client.post(reverse("cashflows"),{'ticker':"TSLA", 'expiration': expiration}, format="json")
        json = response.json()
        self.assertEqual(expiration, json["options"]["expiration"])
