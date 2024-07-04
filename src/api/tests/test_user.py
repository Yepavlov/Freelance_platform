from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user(self):
        user_data = {
            "email": "test@mail.com",
            "first_name": "James",
            "last_name": "Bond",
            "is_staff": True,
            "phone_number": "+15305667755",
            "user_type": 1,
            "password": "some_password1",
            "re_password": "some_password1",
        }
        response = self.client.post("/api/auth/users/", user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], user_data["email"])
        self.assertEqual(response.data["first_name"], user_data["first_name"])
        self.assertEqual(response.data["last_name"], user_data["last_name"])
        self.assertEqual(response.data["is_staff"], user_data["is_staff"])
        self.assertEqual(response.data["phone_number"], user_data["phone_number"])
        self.assertEqual(response.data["user_type"], user_data["user_type"])

    def test_user_invalid_phone_number(self):
        user_data = {
            "email": "test@mail.com",
            "first_name": "James",
            "last_name": "Bond",
            "is_staff": True,
            "phone_number": "123456",
            "user_type": 1,
            "password": "some_password1",
            "re_password": "some_password1",
        }
        response = self.client.post("/api/auth/users/", user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["phone_number"], ["The phone number entered is not valid."])
