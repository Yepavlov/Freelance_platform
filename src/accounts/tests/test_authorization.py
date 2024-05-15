import unittest
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = get_user_model()(email="test@mail.com", user_type=1)
        self.user.set_password("123456789")
        self.user.save()

        self.manager = get_user_model()(email="test1@mail.com", is_staff=True)
        self.manager.set_password("123456789")
        self.manager.save()

    def test_user_login_wrong_email(self):
        user_login = self.client.login(email="wrong@email.com", password="123456789")
        self.assertFalse(user_login)

    def test_user_login_wrong_password(self):
        user_login = self.client.login(email="test@mail.com", password="wrong_password")
        self.assertFalse(user_login)

    def test_user_access_admin_panel(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_manager_access_admin_panel(self):
        self.client.force_login(self.manager)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_type(self):
        self.assertEqual(self.user.user_type, 1)

    def test_user_is_stuff(self):
        self.assertEqual(self.user.is_staff, False)
