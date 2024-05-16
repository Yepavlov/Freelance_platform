from django.test import TestCase

from core.utils.samples import sample_banking_information


class TestBankingInformation(TestCase):
    def setUp(self):
        self.client_banking_information = sample_banking_information(
            account_holder_name="Test Client",
            account_number="123456789",
            bank_name="Bank of America",
            country_name="USA",
            currency=0,
            client_email="client_email@gmail.com",
        )

        self.freelancer_banking_information = sample_banking_information(
            account_holder_name="Test Freelancer",
            account_number="987654321",
            bank_name="Bank of Ukraine",
            country_name="Ukraine",
            currency=1,
            client_email="freelancer_email@gmail.com",
        )

    def test_client_banking_information(self):
        self.assertEqual(self.client_banking_information.account_holder_name, "Test Client")
        self.assertEqual(self.client_banking_information.account_number, "123456789")
        self.assertEqual(self.client_banking_information.bank_name, "Bank of America")
        self.assertEqual(self.client_banking_information.country.name, "USA")
        self.assertEqual(self.client_banking_information.currency, 0)

    def test_freelancer_banking_information(self):
        self.assertEqual(self.freelancer_banking_information.account_holder_name, "Test Freelancer")
        self.assertEqual(self.freelancer_banking_information.account_number, "987654321")
        self.assertEqual(self.freelancer_banking_information.bank_name, "Bank of Ukraine")
        self.assertEqual(self.freelancer_banking_information.country.name, "Ukraine")
        self.assertEqual(self.freelancer_banking_information.currency, 1)
