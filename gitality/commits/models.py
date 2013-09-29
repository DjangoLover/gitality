from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class GithubCommitManager(models.Manager):
    def create_from_real_commit(self, github_commit, author, project):
        commit = self.objects.create(
            additions=github_commit.additions,
            deletions=github_commit.deletions,
            html_url=github_commit.html_url,
            message=github_commit.message,
            sha=github_commit.sha,
            etag=github_commit.etag,
            last_modified=github_commit.last_modified,
            author=author,
            project=project)
        return commit


class CommitAuthor(TimeStampedModel):
    """
    Represents commit (owner) author object.
    """

    # GitHub data
    author_id = models.BigIntegerField(_(u'author id'))
    avatar_url = models.URLField(_(u'avatar url'), blank=True)
    bio = models.TextField(_(u'bio'), blank=True)
    email = models.EmailField(_(u'e-mail'), blank=True)
    gravatar_id = models.CharField(_(u'gravatar id'), max_length=256, blank=True)
    login = models.CharField(_(u'author login'), max_length=256, unique=True)
    name = models.CharField(_(u'author name'), max_length=256, blank=True)
    followers = models.BigIntegerField(_(u'followers count'), default=0)
    following = models.BigIntegerField(_(u'following count'), default=0)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _(u'commit author')
        verbose_name_plural = _(u'commit authors')

    def update_from_commit(self, github_commit):
        author = github_commit.author
        self.avatar_url = getattr(author, 'avatar_url', '')
        self.bio = getattr(author, 'bio', '')
        self.email = getattr(author, 'email', '')
        self.gravatar_id = getattr(author, 'gravatar_id', '')
        self.login = getattr(author, 'login', '')
        self.name = getattr(author, 'name', '')
        self.followers = getattr(author, 'followers', 0)
        self.following = getattr(author, 'following', 0)
        self.save()

    def __unicode__(self):
        return u'{}'.format(self.name or self.login)


class Commit(TimeStampedModel):
    """
    Represents commit object.
    """
    objects = GithubCommitManager()
    # GitHub data
    additions = models.BigIntegerField(_(u'additions'), blank=True, null=True)
    deletions = models.BigIntegerField(_(u'deletions'), blank=True, null=True)
    html_url = models.URLField(_(u'commit url'))
    message = models.TextField(_(u'commit message'), blank=True)
    sha = models.CharField(_(u'commit revision sha'), max_length=256)
    etag = models.CharField(_(u'commit etag'), max_length=256)
    last_modified = models.DateTimeField(_(u'commit last modified'))

    author = models.ForeignKey(CommitAuthor, related_name='commits')
    project = models.ForeignKey('projects.Project', related_name='commits')

    class Meta(TimeStampedModel.Meta):
        verbose_name = _(u'commit')
        verbose_name_plural = _(u'commits')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.author, self.message)
