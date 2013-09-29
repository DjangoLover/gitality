from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from annoying.fields import AutoOneToOneField
from dirtyfields import DirtyFieldsMixin
from south.modelsinspector import add_introspection_rules

from core.models import TimeStampedModel

from .signals import progress_state_changed

add_introspection_rules([], ['^annoying\.fields\.AutoOneToOneField'])


class CommonProgressModel(DirtyFieldsMixin, TimeStampedModel):
    """
    Holds common set of fields
    required for all progress states.
    """

    SKIP_FIELDS = ('created', 'modified', 'id')

    commit_count = models.BigIntegerField(default=0)
    additions_count = models.BigIntegerField(default=0)
    deletions_count = models.BigIntegerField(default=0)

    extra_data = models.ManyToManyField('core.KVS', blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        abstract = True

    def get_entity(self):
        """
        Should be defined in subclasses and
        return corresponding progress entity.
        """
        raise NotImplementedError

    def get_entity_type(self):
        """
        Returns appropriate entity type, that is
        relevant for Achievement.entity field choices.
        """
        return models.get_model(
            'achievements',
            'Achievement'
        ).get_entity_type_map()[self.get_entity().__class__]

    def check_requirement(self, key, value):
        return getattr(self, key) >= value

    def get_dirty_fields_with_new_values(self):
        """
        Returns a dictionary of
        dirty fields with new values.
        """
        # Skipping certain fields
        return {f: getattr(self, f) for f in
                filter(lambda v: v not in self.SKIP_FIELDS,
                       self.get_dirty_fields())}


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

    def get_entity(self):
        return self.author

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

    def get_entity(self):
        return self.project

    def update_state(self):
        raise NotImplementedError


@receiver(models.signals.pre_save, sender=AuthorProgress)
@receiver(models.signals.pre_save, sender=ProjectProgress)
def on_progress_pre_save(sender, **kwargs):
    """
    Handles pre_save signal for progress models.
    """

    progress = kwargs['instance']

    dirty_fields = progress.get_dirty_fields_with_new_values()
    # Sending progress_state_changed signal if something changed
    dirty_fields and progress_state_changed.send(
        sender,
        entity_type=progress.get_entity_type(),
        entity=progress.get_entity(),
        dirty_fields=dirty_fields
    )
