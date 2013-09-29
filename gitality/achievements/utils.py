from django.utils.importlib import import_module


def get_class_by_path(cls_path):
    """
    Returns class by it's path.
    """
    path_fragments = cls_path.split('.')
    cls_name = path_fragments.pop()
    module_path = '.'.join(path_fragments)
    module = import_module(module_path)
    return getattr(module, cls_name)
