from .models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class UserLoginAPIViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("users:users:register")

    def test_register_create_user_should_pass(self):
        data =  {"first_name": "hi", "last_name": "md", "email": "hi@mb.com", "password": "1234", "password2": "1234"}
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_register_create_user_incorrect_email_should_fail(self):
        data =  {"first_name":"hi", "last_name": "md", "email": "hi", "password": "", "password2": "1234"}
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_register_create_user_first_name_missing_should_fail(self):
        data =  {"last_name": "md", "email": "hi", "password": "", "password2": "1234"}
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_register_create_user_last_name_missing_should_fail(self):
        data =  {"first_name":"hi", "email": "hi", "password": "", "password2": "1234"}
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)
    
    def test_register_create_user_email_missing_should_fail(self):
        data =  {"first_name": "hi", "last_name": "md", "password": "1234", "password2": "1234"}
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)
    
    def test_register_create_user_password_missing_should_fail(self):
        data =  {"first_name": "hi", "last_name": "md", "password2": "1234"}
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_register_create_user_password_mismatch_should_fail(self):
        data =  {"first_name": "hi", "last_name": "md", "email": "hi@mb.com", "password": "12345", "password2": "1234"}
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_register_create_user_with_active_email_should_fail(self):
        data =  {"first_name": "hi", "last_name": "mb", "email": "hi@mb.com", "password": "1234", "password2": "1234"}
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

        data =  {"first_name": "hi", "last_name": "md", "email": "hi@mb.com", "password": "1235", "password2": "1235"}
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)