import abc


class BaseAchievementLogic(object):
    """
    Base class for achievement logic classes
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, achievement, entity):
        self.achievement = entity
        self.entity = entity

    @abc.abstractmethod
    def inspect(self):
        raise NotImplementedError
