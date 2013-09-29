import sys

from django.core.management.base import NoArgsCommand

from achievements.models import Achievement
from achievements.tasks import inspect_achievement
from commits.models import Commit, CommitAuthor
from projects.models import Project


def get_fake_dirty_fields(model):
    """
    Returns dict of dirty fields
    for given progress model.
    """
    return {d: None for d in
        filter(lambda f: f not in model.SKIP_FIELDS,
               [f.name for f in model._meta.fields])}


class Command(NoArgsCommand):
    """
    Inspects all the progresses.
    """

    def handle_noargs(self, **options):

        sys.stdout.write('Starting inspections\n')

        achievements = Achievement.objects.prefetch_related('requirements')

        commit_count = Commit.objects.count()
        commit_author_count = CommitAuthor.objects.count()
        project_count = Project.objects.count()

        sys.stdout.write('Inspecting {} commits\n'.format(commit_count))

        # TODO: Implement separate commit achievements inspection
        # for commit in Commit.objects.all():
        #     inspect_achievement.delay(
        #         achievements,
        #         commit.progress.get_entity_type(),
        #         commit.progress.get_entity(),
        #         get_fake_dirty_fields(commit.progress.__class__)
        #     )

        sys.stdout.write('Inspecting {} commit authors\n'.format(commit_author_count))

        for commit_author in CommitAuthor.objects.all():
            inspect_achievement.delay(
                achievements,
                commit_author.progress.get_entity_type(),
                commit_author.progress.get_entity(),
                get_fake_dirty_fields(commit_author.progress.__class__)
            )

        sys.stdout.write('Inspecting {} projects\n'.format(project_count))

        for project in Project.objects.all():
            inspect_achievement.delay(
                achievements,
                project.progress.get_entity_type(),
                project.progress.get_entity(),
                get_fake_dirty_fields(project.progress.__class__)
            )

        sys.stdout.write('Done\n')
