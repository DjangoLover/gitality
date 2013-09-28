from django.db import models
from django.utils.translation import ugettext_lazy as _


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


class KVS(models.Model):
    """
    Basic key-value storage model.
    """

    key = models.CharField(max_length=256)
    value = models.TextField(blank=True)

    class Meta:
        verbose_name = _(u'KVS item')
        verbose_name_plural = _(u'KVS items')

    def __unicode__(self):
        return u'{0}:{1}'.format(self.key, self.value)
