from django.test import TestCase

from core.utils.samples import sample_payment


class TestPayment(TestCase):
    def setUp(self):
        self.payment = sample_payment(
            client_email="client_email@gmail.com",
            amount=500.00,
            payment_method="MasterCard",
        )

    def test_payment_creating(self):
        self.assertEqual(self.payment.amount, 500.00)
        self.assertEqual(self.payment.payment_method, "MasterCard")
        self.assertEqual(self.payment.description, "Payment for contract 1")
        self.assertEqual(self.payment.job.title, "Python dev")
