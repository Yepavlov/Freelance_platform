from django.test import TestCase

from freelancers.utils.samples import sample_review_about_freelancer


class TestReviewAboutFreelancer(TestCase):
    def setUp(self):
        self.review_about_freelancer = sample_review_about_freelancer(
            freelancer_email="freelancer_email@gmail.com",
            client_email="client_email.com",
            rating=9,
        )

    def test_review_about_freelancer(self):
        self.assertEqual(self.review_about_freelancer.rating, 9)
        self.assertEqual(self.review_about_freelancer.review, "some review")
        self.assertEqual(self.review_about_freelancer.from_client.user.email, "client_email.com")
        self.assertEqual(self.review_about_freelancer.to_freelancer.user.email, "freelancer_email@gmail.com")
        self.assertEqual(self.review_about_freelancer.job.title, "Python developer")
