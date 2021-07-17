from django.test import TestCase
from django.urls import reverse
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


class PasswordResetTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testUser','test@gmail.com','secure49password')
        url = 'http://testserver/' + 'api/password_reset/'
        self.response = self.client.post(url, {"email":'test@gmail.com'})
        self.body = mail.outbox[0].body

    def test_user_can_get_reset_email(self):
        cleaned = self.response.content.decode('utf8').replace("'", '"')
        self.assertTrue(cleaned.find("OK") > -1)

    def test_user_reset_password_email_is_valid(self):
        self.assertTrue(self.body.find("http") > -1)
        self.assertTrue(self.body.find("/user/change_password/") > -1)

    def test_user_token_resets(self):
        token = self.body.split("/")[-2]
        url = reverse('password_reset:reset-password-confirm')
        self.client.post(url, {"token":token, "password":"more49secure48password"})
        old_login = self.client.login(username='testUser', password='secure49password')
        self.assertFalse(old_login)
        new_login = self.client.login(username='testUser', password='more49secure48password')
        self.assertTrue(new_login)