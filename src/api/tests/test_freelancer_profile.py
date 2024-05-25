from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from accounts.utils.samples import sample_user
from core.models import Skill
from core.utils.samples_for_location import sample_city


class TestFreelancerProfileAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_freelancer = sample_user(
            email="test_freelancer@mail.com",
            first_name="James",
            last_name="Caron",
            is_staff=True,
            is_active=True,
            user_type=0,
        )
        self.skill = Skill.objects.create(title="Python")
        self.city = sample_city("USA", "CA", "Los Angeles")
        self.freelancer_data = {
            "position": "Python backend developer",
            "description": "Python backend developer description",
            "birth_date": "2000-07-20",
            "hourly_rate": 42.00,
            "country": self.city.state.country.id,
            "state": self.city.state.id,
            "city": self.city.id,
            "sex": 0,
            "skill": [self.skill.id],
        }

    def test_create_freelancer_profile_api(self):
        self.client.force_authenticate(user=self.user_freelancer)
        response = self.client.post(
            reverse("api:create_freelancer_profile"),
            self.freelancer_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["position"], self.freelancer_data["position"])
        self.assertEqual(response.data["description"], self.freelancer_data["description"])
        self.assertEqual(response.data["birth_date"], self.freelancer_data["birth_date"])
        self.assertEqual(
            float(response.data["hourly_rate"]),
            round(self.freelancer_data["hourly_rate"], 2),
        )
        self.assertEqual(response.data["country"], self.city.state.country.id)
        self.assertEqual(response.data["state"], self.city.state.id)
        self.assertEqual(response.data["city"], self.city.id)
        self.assertEqual(response.data["sex"], self.freelancer_data["sex"])
        self.assertEqual(response.data["skill"], [self.skill.id])

    def test_create_freelancer_profile_api_invalid_birth_date(self):
        self.client.force_authenticate(user=self.user_freelancer)
        self.freelancer_data["birth_date"] = "2010-07-20"
        response = self.client.post(
            reverse("api:create_freelancer_profile"),
            self.freelancer_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["birth_date"], ["Person must be at least 14 years old."])

    def test_permission_create_freelancer_profile_api(self):
        user_client = sample_user(
            email="test@mail.com",
            first_name="James",
            last_name="Caron",
            is_staff=True,
            is_active=True,
            user_type=1,
        )
        self.client.force_authenticate(user=user_client)
        response = self.client.post(
            reverse("api:create_freelancer_profile"),
            self.freelancer_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You do not have permission to perform this action.")
