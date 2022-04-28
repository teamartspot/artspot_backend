
from django.urls import reverse
from user.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("auth:login")

    def setUp(self):
        self.first_name = "abc"
        self.last_name = "def"
        self.email = "abc@def.com"
        self.password = "1234"
        self.user = User.objects.user_create( self.first_name,  self.last_name,  self.email, self.password)

    def test_authentication_with_correct_credentials_should_pass(self):
        response = self.client.post(self.url, {"email": "abc@def.com", "password":"1234"})
        self.assertEqual(200, response.status_code)

    def test_authentication_with_incorrect_credentials_should_fail(self):
        response = self.client.post(self.url, {"email": "pp@mk.com", "password":"1234"})
        self.assertEqual(401, response.status_code)

