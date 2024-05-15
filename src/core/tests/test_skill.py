from django.test import TestCase

from core.models import Skill


class TestSkill(TestCase):
    def setUp(self):
        self.skill = Skill(
            title="JAVA",
        )

    def test_skill(self):
        self.assertEqual(self.skill.title, "JAVA")
