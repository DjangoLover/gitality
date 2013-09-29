from django.test import SimpleTestCase

from .logic import CommitCountLogic
from .models import Achievement
from .utils import get_class_by_path


class AchievementsUtilsTest(SimpleTestCase):

    def test_get_class_by_path(self):
        self.assertEqual(
            get_class_by_path('achievements.models.Achievement'),
            Achievement
        )
        self.assertEqual(
            get_class_by_path('achievements.logic.CommitCountLogic'),
            CommitCountLogic
        )
