from django.core.exceptions import ValidationError
from django.test import TestCase

from clients.models import ClientProfile
from clients.utils.samples import sample_client_profile


class TestClientProfile(TestCase):
    def setUp(self):
        self.client_profile = sample_client_profile(
            user_email="test@mail.com",
        )

    def test_client_profile(self):
        self.assertEqual(self.client_profile.company, "Google Inc.")
        self.assertEqual(self.client_profile.image, None)

    def test_client_profile_company_limit(self):
        with self.assertRaises(ValidationError):
            self.freelancer_profile = sample_client_profile(
                user_email="test12@gmail.com",
                company="A" * 256,
            )
        self.assertEqual(ClientProfile.objects.count(), 1)

    def test_client_profile_company_description_limit(self):
        with self.assertRaises(ValidationError):
            self.freelancer_profile = sample_client_profile(
                user_email="test12@gmail.com",
                company_description="A" * 256,
            )
        self.assertEqual(ClientProfile.objects.count(), 1)
