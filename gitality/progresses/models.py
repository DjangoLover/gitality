from django.db import models
from django.utils.translation import ugettext_lazy as _

from annoying.fields import AutoOneToOneField
from south.modelsinspector import add_introspection_rules

from core.models import TimeStampedModel

add_introspection_rules([], ['^annoying\.fields\.AutoOneToOneField'])


class AuthorProgress(TimeStampedModel):
    """
    Represents commit author progress state object.
    """

    author = AutoOneToOneField('commits.CommitAuthor', related_name='progress')

    class Meta(TimeStampedModel.Meta):
        verbose_name = _(u'commit author progress')
        verbose_name_plural = _(u'commit author progresses')

    def __unicode__(self):
        return u'Progress for {}'.format(self.author)


class ProjectProgress(TimeStampedModel):
    """
    Represents project progress state object.
    """

    project = AutoOneToOneField('projects.Project', related_name='progress')

    last_commits_update = models.DateTimeField(blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _(u'project progress')
        verbose_name_plural = _(u'project progresses')

    def __unicode__(self):
        return u'Progress for {}'.format(self.project)
