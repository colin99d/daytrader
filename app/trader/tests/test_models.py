from trader.models import Algorithm, Decision, Stock
from trader.functions.helpers import last_date
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
        self.decision = Decision.objects.create(stock=self.stock,algorithm=self.algo,openPrice=10,confidence=.2,tradeDate=self.tradeDate, long=True)
        self.assertEqual(str(self.stock) + ' on ' + str(self.tradeDate), self.decision.__str__())

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
        self.assertTrue(Stock.objects.get(ticker="AEGN").listed == False)
        self.assertTrue(Stock.objects.get(ticker="APXTU").listed == False)