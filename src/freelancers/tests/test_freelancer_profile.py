from django.core.exceptions import ValidationError
from django.test import TestCase

from freelancers.models import FreelancerProfile
from freelancers.utils.samples import sample_freelancer_profile


class TestFreelancerProfile(TestCase):
    def setUp(self):
        self.freelancer_profile = sample_freelancer_profile(
            user_email="test@gmail.com",
            position="Python developer",
            hourly_rate=25.00,
            location="San diego, CA, USA",
            sex=0,
        )

    def test_freelancer_profile(self):
        self.assertEqual(self.freelancer_profile.sex, 0)
        self.assertEqual(self.freelancer_profile.position, "Python developer")
        self.assertEqual(self.freelancer_profile.hourly_rate, 25.00)
        self.assertEqual(self.freelancer_profile.location, "San diego, CA, USA")

    def test_freelancer_profile_position_limit(self):
        with self.assertRaises(ValidationError):
            self.freelancer_profile = sample_freelancer_profile(
                user_email="test12@gmail.com",
                position="P" * 256,
                hourly_rate=15.00,
                location="Los Angeles, CA, USA",
                sex=1,
            )
        self.assertEqual(FreelancerProfile.objects.count(), 1)

    def test_freelancer_profile_hourly_rate_limit(self):
        with self.assertRaises(ValidationError):
            self.freelancer_profile = sample_freelancer_profile(
                user_email="test12@gmail.com",
                position="Python developer",
                hourly_rate=123456,
                location="Los Angeles, CA, USA",
                sex=1,
            )
        self.assertEqual(FreelancerProfile.objects.count(), 1)

    def test_freelancer_profile_birth_date_limit(self):
        """
        Input birth_date less than 14 years old.
        """
        with self.assertRaises(ValidationError):
            self.freelancer_profile = sample_freelancer_profile(
                user_email="test12@gmail.com",
                position="Python developer",
                hourly_rate=15.00,
                location="Los Angeles, CA, USA",
                sex=1,
                birth_date="2011-03-07",
            )
        self.assertEqual(FreelancerProfile.objects.count(), 1)
