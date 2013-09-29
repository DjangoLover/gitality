from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel
from core.utils import cached_property

from .utils import get_logic_choices


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

    logic_class = models.CharField(
        _(u'achievement logic class'),
        choices=get_logic_choices(),
        max_length=256)

    requirements = models.ManyToManyField('core.KVS')

    class Meta(TimeStampedModel.Meta):
        verbose_name = _(u'achievement')
        verbose_name_plural = _(u'achievements')

    def __unicode__(self):
        return u'{}'.format(self.name)

    @property
    def logic(self):
        """
        Returns achievement logic instance.
        """
        return self.logic_class(self)

    @cached_property(ttl=0)
    def requirements_dict(self):
        """
        Returns requirements as a dict {key: value}
        """
        return {kv.key: kv.value for kv in
                self.requirements.only('key', 'value_raw')}


class EntityAchievementModel(TimeStampedModel):
    """
    Base entity achievement model class.
    """

    achievement = models.ForeignKey(Achievement)

    class Meta(TimeStampedModel.Meta):
        abstract = True


class CommitAchievement(EntityAchievementModel):
    """
    Represents unlocked achievement by commit
    """

    commit = models.ForeignKey('commits.Commit', related_name='achievements')

    class Meta(EntityAchievementModel.Meta):
        unique_together = ('achievement', 'commit')
        verbose_name = _(u'commit achievement')
        verbose_name_plural = _(u'commit achievements')

    def __unicode__(self):
        return u'Commit achievement {0} for {1}'.format(self.achievement, self.commit)


class CommitAuthorAchievement(EntityAchievementModel):
    """
    Represents unlocked achievement by commit author
    """

    author = models.ForeignKey('commits.CommitAuthor', related_name='achievements')

    class Meta(EntityAchievementModel.Meta):
        unique_together = ('achievement', 'author')
        verbose_name = _(u'commit author achievement')
        verbose_name_plural = _(u'commit author achievements')

    def __unicode__(self):
        return u'Commit author achievement {0} for {1}'.format(
            self.achievement,
            self.author
        )


class ProjectAchievement(EntityAchievementModel):
    """
    Represents unlocked achievement by project
    """

    project = models.ForeignKey('projects.Project', related_name='achievements')

    class Meta(EntityAchievementModel.Meta):
        unique_together = ('achievement', 'project')
        verbose_name = _(u'project achievement')
        verbose_name_plural = _(u'project achievements')

    def __unicode__(self):
        return u'Project achievement {0} for {1}'.format(
            self.achievement,
            self.project
        )
