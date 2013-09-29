from django.db import models
from django.utils.translation import ugettext_lazy as _

from annoying.fields import AutoOneToOneField
from south.modelsinspector import add_introspection_rules

from core.models import TimeStampedModel, KVS

add_introspection_rules([], ['^annoying\.fields\.AutoOneToOneField'])


class CommonProgressModel(TimeStampedModel):
    """
    Holds common set of fields
    required for all progress states.
    """

    commit_count = models.BigIntegerField(default=0)
    additions_count = models.BigIntegerField(default=0)
    deletions_count = models.BigIntegerField(default=0)

    extra_data = models.ManyToManyField(KVS, blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        abstract = True


class AuthorProgress(CommonProgressModel):
    """
    Represents commit author progress state object.
    """

    author = AutoOneToOneField('commits.CommitAuthor', related_name='progress')

    class Meta(CommonProgressModel.Meta):
        verbose_name = _(u'commit author progress')
        verbose_name_plural = _(u'commit author progresses')

    def __unicode__(self):
        return u'Progress for {}'.format(self.author)

    def update_state(self):
        raise NotImplementedError


class ProjectProgress(CommonProgressModel):
    """
    Represents project progress state object.
    """

    project = AutoOneToOneField('projects.Project', related_name='progress')

    last_commit_update = models.DateTimeField(blank=True, null=True)

    class Meta(CommonProgressModel.Meta):
        verbose_name = _(u'project progress')
        verbose_name_plural = _(u'project progresses')

    def __unicode__(self):
        return u'Progress for {}'.format(self.project)

    def update_state(self):
        raise NotImplementedError
