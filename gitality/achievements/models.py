from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class Achievement(TimeStampedModel):
    """
    Represents achievement object.
    """

    COMMIT, COMMIT_AUTHOR, PROJECT = range(1, 4)
    ENTITY_CHOICES = (
        (COMMIT, _(u'commit')),
        (COMMIT, _(u'commit author')),
        (COMMIT, _(u'project')),
    )

    key = models.CharField(
        _(u'achievement key'),
        max_length=256,
        db_index=True,
        unique=True)

    name = models.CharField(_(u'achievement name'), max_length=128, unique=True)
    description = models.TextField(_(u'achievement description'), blank=True)

    entity = models.PositiveSmallIntegerField(
        _(u'affected entity'),
        choices=ENTITY_CHOICES,
        default=COMMIT_AUTHOR)

    points = models.PositiveIntegerField(_(u'points'), default=10)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _(u'achievement')
        verbose_name_plural = _(u'achievements')

    def __unicode__(self):
        return u'{}'.format(self.name)
