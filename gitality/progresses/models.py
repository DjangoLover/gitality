from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

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

    def increment_counters(self, github_commit):
        self.additions_count += github_commit.additions
        self.deletions_count += github_commit.deletions
        self.commit_count += 1

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

    def update_state(self, github_commit):
        self.increment_counters(github_commit)
        self.save()

    def get_entity(self):
        return self.author


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

    @property
    def iso_date(self):
        date = None
        if self.last_commit_update:
            date = str(self.last_commit_update).split(' ')
            date = 'T'.join(date)
        return date

    def update_state(self):
        from commits.models import CommitAuthor, Commit
        repo = self.project.github_repo_obj
        if not (repo and repo.size):
            return
        commits = repo.iter_commits(since=self.iso_date)
        for com in commits:
            com = repo.commit(com.sha)
            if not com.author:
                continue
            author, created = CommitAuthor.objects.get_or_create(
                author_id=com.author.id)
            if created:
                author.update_from_commit(com)
            Commit.objects.create_from_real_commit(
                com, author, self.project)
            self.increment_counters(com)
            author.progress.update_state(com)
        self.last_commit_update = timezone.now()
        self.save()

    def get_entity(self):
        return self.project


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
