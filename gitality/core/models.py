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

    TYPE_MAP = (
        ('int', int),
        ('float', float)
    )

    TYPE_CHOICES = tuple((t, t) for t in dict(TYPE_MAP).keys())

    key = models.CharField(max_length=256, db_index=True)
    value_raw = models.TextField(_(u'raw value'), blank=True)
    value_type = models.CharField(
        _(u'value type'),
        choices=TYPE_CHOICES,
        help_text=_(u'Coerces raw value to given type if needed'),
        max_length=32,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _(u'KVS item')
        verbose_name_plural = _(u'KVS items')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.key, self.value)

    @property
    def value(self):
        """
        Coerces raw value to appropriate type if
        given, otherwise returns raw value (string)
        """
        return (
            self.value_raw if self.value_type is None
            else dict(self.TYPE_MAP)[self.value_type](self.value_raw)
        )
