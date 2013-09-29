from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now

from mock import Mock, patch

from .models import CommonProgressModel, ProjectProgress
from commits.models import CommitAuthor
from projects.models import Project


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
        progress = ProjectProgress()
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
        u, _ = User.objects.get_or_create(username='gitality')
        proj, _ = Project.objects.get_or_create(
            name='Test', repo_url='https://github.com/dmrz/gitality',
            user=u)
        progress = proj.progress
        self.assertEqual(progress.commit_count, 0)
        self.assertEqual(progress.additions_count, 0)
        self.assertEqual(progress.deletions_count, 0)
        mock_repo.iter_commits.side_effect = _return_mocks
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
