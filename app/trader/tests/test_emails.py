from trader.models import Algorithm, Decision, Stock
from trader.functions.helpers import daily_email
from django.utils.timezone import make_aware
from django.test import TransactionTestCase
from datetime import datetime
from django.core import mail
from user.models import User


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
        """Add"""

    def test_email_correct_algo(self):
        """Tests that an email chooses the correct algorithm to send"""
        algo1 = Algorithm.objects.create(name="Test the algo")
        algo2 = Algorithm.objects.create(name="Test this algo also")
        setattr(self.user,"selected_algo",algo1)
        self.user.save()
        daily_email(self.user)
        self.assertTrue(algo1.name in mail.outbox[0].body)

    def test_email_filters_decisions(self):
        """Tests that the email only sends decisions that are from the selected algorithm"""
        algo1 = Algorithm.objects.create(name="Test the algo")
        algo2 = Algorithm.objects.create(name="Test this algo also")
        stock1 = Stock.objects.create(ticker="IWV", listed=True)
        stock2 = Stock.objects.create(ticker="CMAX", listed=True)
        stock3 = Stock.objects.create(ticker="CANO", listed=True)
        stock4 = Stock.objects.create(ticker="AAPL", listed=True)
        Decision.objects.create(stock=stock1, algorithm=algo1, tradeDate=make_aware(datetime(2021, 7, 6, 12, 0)), long=True)
        Decision.objects.create(stock=stock2, algorithm=algo1, tradeDate=make_aware(datetime(2021, 7, 7, 12, 0)), long=True)
        Decision.objects.create(stock=stock3, algorithm=algo2, tradeDate=make_aware(datetime(2021, 7, 6, 12, 0)), long=True)
        Decision.objects.create(stock=stock4, algorithm=algo2, tradeDate=make_aware(datetime(2021, 7, 7, 12, 0)), long=True)
        setattr(self.user,"selected_algo",algo1)
        self.user.save()
        daily_email(self.user)
        body = mail.outbox[0].body
        self.assertTrue(stock1.ticker in body)
        self.assertTrue(stock2.ticker in body)
        self.assertTrue(stock3.ticker not in body)
        self.assertTrue(stock4.ticker not in body)