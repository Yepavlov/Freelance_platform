from django.core.exceptions import ValidationError
from django.test import TestCase

from clients.models import Job
from clients.utils.samples import sample_job


class TestJob(TestCase):
    def setUp(self):
        self.job = sample_job(
            user_email="firstemail@gmail.com",
            title="Python developer",
            description="Creating a web application",
            hourly_rate=52.00,
            estimated_end_date="2024-09-25",
        )

    def test_job(self):
        self.assertEqual(self.job.title, "Python developer")
        self.assertEqual(self.job.description, "Creating a web application")
        self.assertEqual(self.job.hourly_rate, 52.00)
        self.assertEqual(str(self.job.estimated_end_date), "2024-09-25")

    def test_job_title_limit(self):
        with self.assertRaises(ValidationError):
            self.job_2 = sample_job(
                user_email="someemail@gmail.com",
                title="P" * 256,
                description="Creating a db",
                hourly_rate=48.00,
                estimated_end_date="2024-07-30",
            )
        self.assertEqual(Job.objects.count(), 1)

    def test_job_hourly_rate_limit(self):
        with self.assertRaises(ValidationError):
            self.job_2 = sample_job(
                user_email="someemail@gmail.com",
                title="Python developer",
                description="Creating a db",
                hourly_rate=123456,
                estimated_end_date="2024-07-30",
            )
        self.assertEqual(Job.objects.count(), 1)

    def test_job_is_concluded_true(self):
        self.job_2 = sample_job(
            user_email="someemail@gmail.com",
            title="Python developer",
            description="Creating a db",
            is_concluded=True,
            hourly_rate=40.00,
            estimated_end_date="2024-07-30",
        )
        self.assertEqual(self.job_2.is_concluded, True)

    def test_job_skill_checking(self):
        self.assertEqual(self.job.skill.first().title, "Python")
