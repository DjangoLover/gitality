from django.db import models


class TimeStampedModel(models.Model):
    """
    Base abstract model that provides
    created and modified fields.
    NOTE: Inherit subclasseses Meta from
    TimeStampedModel.Meta when overriding.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created']
