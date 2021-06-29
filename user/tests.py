from rest_framework.test import RequestsClient
from django.contrib.auth.models import User
from django.test import TestCase


class TestAuthentication(TestCase):
    def setUp(self):
        User.objects.create_user('test1','test@test.com','qwe123qwe')

    def test_user_can_login(self):
        user = User.objects.first()
        self.assertEqual(User.objects.count(), 1)
        url = 'http://testserver/' + 'token-auth/'
        response = self.client.post(url, {"username":'test1',"password":'qwe123qwe'})
        cleaned = response.content.decode('utf8').replace("'", '"')
        self.assertTrue(cleaned.find("token") > -1)