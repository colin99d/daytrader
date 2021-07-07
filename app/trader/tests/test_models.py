from trader.models import Algorithm, Decision, Stock
from django.utils import timezone
from django.test import TestCase

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