from django.db import models
from django.utils.translation import ugettext_lazy as _
from dajngo.utils.timezone import now

from annoying.fields import AutoOneToOneField
from south.modelsinspector import add_introspection_rules

from core.models import TimeStampedModel, KVS
from commits.models import CommitAuthor, Commit

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

    def update_state(self, github_commit):
        self.commit_count += 1
        self.additions_count += github_commit.additions
        self.deletions_count += github_commit.deletions
        self.save()


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
        repo = self.project.github_repo_obj()
        for com in repo.iter_commits(since=self.iso_date):
            author, created = CommitAuthor.objects.get_or_create(
                author_id=com.author.id)
            if created:
                author.update_from_commit(com)
            Commit.objects.create(
                additions=com.additions,
                deletions=com.deletions,
                html_url=com.html_url,
                message=com.message,
                sha=com.sha,
                etag=com.etag,
                last_modified=com.last_modified,
                author=author,
                project=self.project)
            author.progress.update_state(com)
            self.commit_count += 1
            self.additions_count += com.additions
            self.deletions_count += com.deletions
        self.last_commit_update = now()
        self.save()
