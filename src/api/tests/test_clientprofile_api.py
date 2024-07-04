from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.utils.samples import sample_user
from core.utils.samples_for_location import sample_city


class TestClientProfileAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_client = sample_user(
            email="test@mail.com",
            first_name="James",
            last_name="Caron",
            is_staff=True,
            is_active=True,
            user_type=1,
        )
        self.city = sample_city("USA", "CA", "Los Angeles")
        self.client_data = {
            "company": "Samsung",
            "company_description": "Samsung description",
            "country": self.city.state.country.id,
            "state": self.city.state.id,
            "city": self.city.id,
        }

    def test_create_client_profile_api(self):
        self.client.force_authenticate(user=self.user_client)
        response = self.client.post(reverse("api:create_client_profile"), self.client_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["company"], self.client_data["company"])
        self.assertEqual(
            response.data["company_description"],
            self.client_data["company_description"],
        )
        self.assertEqual(response.data["country"], self.city.state.country.id)
        self.assertEqual(response.data["state"], self.city.state.id)
        self.assertEqual(response.data["city"], self.city.id)

    def test_permission_create_client_profile_api(self):
        user_freelancer = sample_user(
            email="test_freelancer@mail.com",
            first_name="James",
            last_name="Caron",
            is_staff=True,
            is_active=True,
            user_type=0,
        )
        self.client.force_authenticate(user=user_freelancer)
        response = self.client.post(reverse("api:create_client_profile"), self.client_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You do not have permission to perform this action.")
