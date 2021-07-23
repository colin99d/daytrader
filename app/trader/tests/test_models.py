from trader.models import Algorithm, Decision, Stock
from trader.functions.helpers import last_date
from django.utils import timezone
from django.test import TestCase
from datetime import datetime

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
        self.trade_date = timezone.now().date()
        self.decision = Decision.objects.create(stock=self.stock,algorithm=self.algo,open_price=10,confidence=.2,trade_date=self.trade_date, long=True)
        self.assertEqual(str(self.stock) + ' on ' + str(self.trade_date), self.decision.__str__())

    def test_update_stock_info(self):
        """Tests that the model method update_stock_info properly modifieds database with results"""
        Stock.objects.create(ticker="TSLA")
        Stock.objects.create(ticker="IWV")
        Stock.objects.create(ticker="Zewff")
        stocks = Stock.objects.all()
        x = last_date(timezone.now())
        for stock in stocks:
            stock.update_stock_info()
        for stock in Stock.objects.all():
            if stock.active:
                self.assertTrue(stock.price > 0)
                self.assertTrue(stock.volume > 0)
                self.assertEqual(stock.last_updated.date(),x[0])
            else:
                self.assertEqual(stock.price, None)
                self.assertEqual(stock.volume, None)
                self.assertEqual(stock.last_updated, None)

    def test_old_datetime_marked_delisted(self):
        s1 = Stock.objects.create(ticker="AEGN")
        s2= Stock.objects.create(ticker="APXTU")
        s1.update_stock_info()
        s2.update_stock_info()
        self.assertFalse(Stock.objects.get(ticker="AEGN").listed)
        self.assertFalse(Stock.objects.get(ticker="APXTU").listed)

    def test_get_info(self):
        s1 = Stock.objects.create(ticker="CMAX")
        s2= Stock.objects.create(ticker="ZZZZ")
        responses = [x.get_info() for x in [s1, s2]]
        self.assertTrue(isinstance(responses[0]["time"],datetime))
        self.assertTrue(responses[0]["price"] > 0)
        self.assertTrue(responses[0]["volume"] > 0)
        self.assertEqual(responses[1], None)

    def test_get_options_chain(self):
        s1 = Stock.objects.create(ticker="CMAX")
        s2 = Stock.objects.create(ticker="TSLA")
        responses = [x.get_options_chain() for x in [s1,s2]]
        self.assertIsNone(responses[0])
        self.assertTrue(len(responses[1]["expirations"]) > 0)
        self.assertTrue(len(responses[1]["calls"]) > 0)
        self.assertTrue(len(responses[1]["puts"]) > 0)
        self.assertTrue(int(responses[1]["expiration"]) > 0)

    def test_get_options_chain_specific_expiration(self):
        s1 = Stock.objects.create(ticker="TSLA")
        response1 = s1.get_options_chain()
        expiration = response1["expirations"][4]
        response2 = s1.get_options_chain(expiration)
        self.assertEqual(expiration,response2["expiration"])