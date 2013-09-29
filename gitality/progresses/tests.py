from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now

from mock import Mock, patch

from achievements.models import Achievement

from commits.models import CommitAuthor
from projects.factories import ProjectFactory
from projects.models import Project

from .tasks import update_projects_state
from .models import CommonProgressModel, ProjectProgress


class ProgressModelsTest(TestCase):
    def test_increment_counters(self):
        progress = CommonProgressModel()
        self.assertEqual(progress.commit_count, 0)
        self.assertEqual(progress.additions_count, 0)
        self.assertEqual(progress.deletions_count, 0)
        commit = Mock()
        commit.additions = 2
        commit.deletions = 3
        progress.increment_counters(commit)
        self.assertEqual(progress.commit_count, 1)
        self.assertEqual(progress.additions_count, 2)
        self.assertEqual(progress.deletions_count, 3)

    def test_iso_date(self):
        u, _ = User.objects.get_or_create(username='gitality')
        proj, _ = Project.objects.get_or_create(
            name='Test', repo_url='https://github.com/dmrz/gitality',
            user=u)
        progress = proj.progress
        self.assertEqual(progress.iso_date, None)
        time = now()
        progress.last_commit_update = time
        self.assertEqual(progress.iso_date, 'T'.join(str(time).split(' ')))

    @patch('progresses.models.AuthorProgress.increment_counters')
    def test_author_update_state(self, mock_inc):
        author = CommitAuthor.objects.create(
            author_id=1, login='welp')
        progress = author.progress
        self.assertEqual(progress.commit_count, 0)
        self.assertEqual(progress.additions_count, 0)
        self.assertEqual(progress.deletions_count, 0)
        progress.update_state('blah')
        mock_inc.assert_called_once_with('blah')

    @patch('commits.models.CommitAuthor.update_from_commit')
    @patch('projects.models.Project.github_repo_obj')
    @patch('commits.models.GithubCommitManager.create_from_real_commit')
    def test_project_update_state(self, mock_create, mock_repo, mock_update):
        authors_before = CommitAuthor.objects.count()

        def _return_mocks(since=None):
            commit = Mock()
            commit.author.id = 4
            commit.author.login = 'asdasd'
            commit.additions = 2
            commit.deletions = 3
            return [commit]

        def _return_mock(since=None):
            return _return_mocks()[0]

        u, _ = User.objects.get_or_create(username='gitality')
        proj, _ = Project.objects.get_or_create(
            name='Test', repo_url='https://github.com/dmrz/gitality',
            user=u)
        progress = proj.progress
        self.assertEqual(progress.commit_count, 0)
        self.assertEqual(progress.additions_count, 0)
        self.assertEqual(progress.deletions_count, 0)
        mock_repo.iter_commits.side_effect = _return_mocks
        mock_repo.commit.side_effect = _return_mock
        # Run update state
        progress.update_state()
        self.assertTrue(mock_repo.iter_commits.called)
        self.assertEqual(
            CommitAuthor.objects.count() - authors_before, 1)
        latest_author = CommitAuthor.objects.latest()
        self.assertEqual(latest_author.author_id, 4)
        mock_update.assert_called_once()
        mock_create.assert_called_once()
        self.assertEqual(progress.commit_count, 1)
        self.assertEqual(progress.additions_count, 2)
        self.assertEqual(progress.deletions_count, 3)

    @patch('projects.models.Project.github_repo_obj')
    def test_project_update_state_empty_repo(self, mock_repo):
        u, _ = User.objects.get_or_create(username='gitality')
        proj, _ = Project.objects.get_or_create(
            name='Test', repo_url='https://github.com/dmrz/gitality',
            user=u)
        progress = proj.progress
        mock_repo.size = 0
        progress.update_state()
        self.assertFalse(mock_repo.iter_commits.called)


class ProgressTasksTest(TestCase):
    @patch('progresses.models.ProjectProgress.update_state')
    def test_update_projects_state(self, mock_update):
        u, _ = User.objects.get_or_create(username='gitality')
        proj, _ = Project.objects.get_or_create(
            name='Test', repo_url='https://github.com/dmrz/gitality',
            user=u)
        self.assertTrue(proj.progress)
        self.assertEqual(ProjectProgress.objects.count(), 1)
        update_projects_state()
        mock_update.assert_called_once_with()


class CommonProgressModelTest(TestCase):

    def setUp(self):
        self.project = ProjectFactory.create()

    def test_project_progress_dirty_fields(self):
        self.assertEqual(self.project.progress.commit_count, 0)
        self.assertDictEqual(
            self.project.progress.get_dirty_fields_with_new_values(),
            {}
        )
        self.project.progress.commit_count += 1
        self.assertDictEqual(
            self.project.progress.get_dirty_fields_with_new_values(),
            {'commit_count': 1}
        )

    @patch('progresses.models.progress_state_changed.send')
    def test_progress_state_changed_signal_sent(self, send_patched):
        self.project.progress.save()
        self.project.progress.commit_count += 1
        self.project.progress.save()
        self.assertTrue(send_patched.called)
        send_patched.assert_called_once_with(
            ProjectProgress,
            entity_type=Achievement.PROJECT,
            entity=self.project,
            dirty_fields={'commit_count': 1})
