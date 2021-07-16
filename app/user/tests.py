from django.test import TestCase
from user.models import User
from django.core import mail


class TestAuthentication(TestCase):
    def setUp(self):
        User.objects.create_user('test1','test@test.com','qwe123qwe')

    def test_user_can_login(self):
        self.assertEqual(User.objects.count(), 1)
        url = 'http://testserver/' + 'api-token-auth/'
        response = self.client.post(url, {"username":'test1',"password":'qwe123qwe'})
        cleaned = response.content.decode('utf8').replace("'", '"')
        self.assertTrue(cleaned.find("token") > -1)

    def test_user_can_reset_password(self):
        url = 'http://testserver/' + 'api/password_reset/'
        response = self.client.post(url, {"email":'test@test.com'})
        cleaned = response.content.decode('utf8').replace("'", '"')
        self.assertTrue(cleaned.find("OK") > -1)

    def test_user_reset_password_email_is_valid(self):
        url = 'http://testserver/' + 'api/password_reset/'
        self.client.post(url, {"email":'test@test.com'})
        body = mail.outbox[0].body
        self.assertTrue(body.find("http") > -1)
        self.assertTrue(body.find("/api/password_reset/?token=") > -1)