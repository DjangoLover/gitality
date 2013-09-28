from django.db import models
from django.utils.translation import ugettext_lazy as _


class CommitAuthor(models.Model):
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

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']
        verbose_name = _(u'commit author')
        verbose_name_plural = _(u'commit authors')

    def __unicode__(self):
        return u'{}'.format(self.name or self.login)


class Commit(models.Model):
    """
    Represents commit object.
    """

    # GitHub data
    additions = models.BigIntegerField(_(u'additions'), blank=True, null=True)
    deletions = models.BigIntegerField(_(u'deletions'), blank=True, null=True)
    html_url = models.URLField(_(u'commit url'))
    message = models.TextField(_(u'commit message'), blank=True)
    sha = models.CharField(_(u'commit revision sha'), max_length=256)
    etag = models.CharField(_(u'commit etag'), max_length=256)
    last_modified = models.DateTimeField(_(u'commit last modified'))

    author = models.ForeignKey(CommitAuthor, related_name='commits')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_lates_by = 'created'
        ordering = ['-created']
        verbose_name = _(u'commit')
        verbose_names = _(u'commits')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.author, self.message)
