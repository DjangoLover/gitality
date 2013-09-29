from django.test import SimpleTestCase

from .base import BaseAchievementLogic
from .logic import CommitCountLogic
from .models import Achievement
from .utils import (
    get_class_by_path,
    check_achievement_logic_class,
    get_logic_choices
)


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

    def test_get_logic_choices(self):
        choices = get_logic_choices()
        choices_dict = dict(choices)
        self.assertIn('achievements.logic.CommitCountLogic', choices_dict.keys())
        self.assertIn('CommitCountLogic', choices_dict.values())

    def test_check_achievement_logic_class(self):
        self.assertTrue(check_achievement_logic_class(CommitCountLogic))
        self.assertFalse(check_achievement_logic_class(Achievement))
        self.assertFalse(check_achievement_logic_class(BaseAchievementLogic))
        self.assertFalse(check_achievement_logic_class(1))
