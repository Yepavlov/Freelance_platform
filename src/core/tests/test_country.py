from django.test import TestCase

from core.utils.samples_for_location import sample_country


class TestCountry(TestCase):

    def test_country(self):
        self.country = sample_country("USA")
        self.assertEqual(self.country.name, "USA")
