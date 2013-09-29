from .tasks import inspect_achievement


class AchievementsEngine(object):
    """
    Handles progress state changes,
    inspects and unlocks achievements.
    """

    def __init__(self, achievements):
        self.achievements = achievements

    def handle(self, **kwargs):
        """
        Serves as a signal receiver handler.
        """
        inspect_achievement.delay(
            self.achievements,
            kwargs['entity_type'],
            kwargs['entity'],
            kwargs['dirty_fields']
        )
