from django.test import TestCase

from core.utils.samples import sample_banking_information


class TestBankingInformation(TestCase):
    def setUp(self):
        self.client_banking_information = sample_banking_information(
            account_holder_name="Test Client",
            account_number="123456789",
            bank_name="Bank of America",
            country="USA",
            currency="USD",
            client_email="client_email@gmail.com",
        )

        self.freelancer_banking_information = sample_banking_information(
            account_holder_name="Test Freelancer",
            account_number="987654321",
            bank_name="Bank of Ukraine",
            country="Ukraine",
            currency="UAH",
            client_email="freelancer_email@gmail.com",
        )

    def test_client_banking_information(self):
        self.assertEqual(self.client_banking_information.account_holder_name, "Test Client")
        self.assertEqual(self.client_banking_information.account_number, "123456789")
        self.assertEqual(self.client_banking_information.bank_name, "Bank of America")
        self.assertEqual(self.client_banking_information.country, "USA")
        self.assertEqual(self.client_banking_information.currency, "USD")

    def test_freelancer_banking_information(self):
        self.assertEqual(self.freelancer_banking_information.account_holder_name, "Test Freelancer")
        self.assertEqual(self.freelancer_banking_information.account_number, "987654321")
        self.assertEqual(self.freelancer_banking_information.bank_name, "Bank of Ukraine")
        self.assertEqual(self.freelancer_banking_information.country, "Ukraine")
        self.assertEqual(self.freelancer_banking_information.currency, "UAH")
