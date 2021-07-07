from trader.functions.helpers import daily_email
from django.test import TransactionTestCase
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
        """Animals that can speak are correctly identified"""

