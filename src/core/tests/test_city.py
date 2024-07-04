from django.test import TestCase

from core.utils.samples_for_location import sample_city


class TestCity(TestCase):

    def test_country(self):
        self.city = sample_city("USA", "CA", "Los Angeles")
        self.assertEqual(self.city.name, "Los Angeles")
