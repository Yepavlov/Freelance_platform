from django.core.exceptions import ValidationError
from django.test import TestCase

from freelancers.models import Proposal
from freelancers.utils.samples import sample_proposal


class TestProposal(TestCase):
    def setUp(self):
        self.proposal = sample_proposal(
            freelancer_email="freelancer_email@gmail.com",
            client_email="client_email@gmail.com",
            hourly_rate=40.00,
            estimated_end_date="2024-09-20",
        )

    def test_proposal_creating(self):
        self.assertEqual(self.proposal.hourly_rate, 40.00)
        self.assertEqual(str(self.proposal.estimated_end_date), "2024-09-20")
        self.assertEqual(self.proposal.title, "Python developer in test description")
        self.assertEqual(self.proposal.job_id.description, "Creating web application")

    def test_proposal_title_limit(self):
        with self.assertRaises(ValidationError):
            self.proposal_2 = sample_proposal(
                freelancer_email="freelancer2_email@gmail.com",
                client_email="client2_email@gmail.com",
                hourly_rate=42.00,
                title="A" * 256,
                estimated_end_date="2024-06-15",
            )
        self.assertEqual(Proposal.objects.count(), 1)

    def test_proposal_hourly_rate_limit(self):
        with self.assertRaises(ValidationError):
            self.proposal_2 = sample_proposal(
                freelancer_email="freelancer2_email@gmail.com",
                client_email="client2_email@gmail.com",
                hourly_rate=123456,
                estimated_end_date="2024-06-15",
            )
        self.assertEqual(Proposal.objects.count(), 1)

    def test_proposal_selected_true(self):
        self.proposal_2 = sample_proposal(
            freelancer_email="freelancer2_email@gmail.com",
            client_email="client2_email@gmail.com",
            hourly_rate=45.00,
            selected=True,
            estimated_end_date="2024-06-15",
        )
        self.assertEqual(self.proposal_2.selected, True)
