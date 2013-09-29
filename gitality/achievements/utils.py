import inspect

from django.utils.importlib import import_module

from .base import BaseAchievementLogic


def get_class_by_path(cls_path):
    """
    Returns class by it's path.
    """
    path_fragments = cls_path.split('.')
    cls_name = path_fragments.pop()
    module_path = '.'.join(path_fragments)
    module = import_module(module_path)
    return getattr(module, cls_name)


def check_achievement_logic_class(logic_class):
    """
    Checks that given achievement logic
    class is valid. Returns boolean.
    """
    return (
        inspect.isclass(logic_class) and
        issubclass(logic_class, BaseAchievementLogic) and
        logic_class != BaseAchievementLogic
    )


def get_logic_choices():
    """
    Returns a tuple of 2-element tuples
    e.g. (logic_class_path, logic_class_name),
    to be used in model field choices.
    """

    from achievements import logic

    return tuple(('{0}.{1}'.format(member.__module__, name), name)
                 for name, member in inspect.getmembers(logic,
                    predicate=check_achievement_logic_class))
