import abc


class BaseAchievementLogic(object):
    """
    Base class for achievement logic classes
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, achievement):
        self.achievement = achievement

    def get_requirements(self):
        """
        Returns achievement requirements
        """
        return self.achievement.requirements_dict

    def inspect(self, entity):
        """
        Checks whether entity progress state
        fields meet achievement requirements.
        """

        for key, value in self.get_requirements().iteritems():
            if not entity.progress.check_requirement(key, value):
                return

        self.unlock(entity)

    def unlock(self, entity):
        """
        Unlocks achievement
        """
