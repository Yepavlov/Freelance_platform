from django.test import TestCase
from djmoney.money import Money

from core.utils.samples import sample_payment


class TestPayment(TestCase):
    def setUp(self):
        self.payment = sample_payment(
            client_email="client_email@gmail.com",
            amount=500.00,
            method="MasterCard",
        )
        self.expected_amount = Money("500.0", "USD")

    def test_payment_creating(self):
        self.assertEqual(self.payment.amount, self.expected_amount)
        self.assertEqual(self.payment.method, "MasterCard")
        self.assertEqual(self.payment.description, "Payment for contract 1")
        self.assertEqual(self.payment.job.title, "Python dev")
