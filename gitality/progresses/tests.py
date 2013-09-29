from django.test import SimpleTestCase

from mock import Mock, patch

from .models import CommonProgressModel, ProjectProgress
from commits.models import CommitAuthor


class ProgressModelsTest(SimpleTestCase):
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

    def test_iso_date(self):
        progress = ProjectProgress()
        self.assertEqual(progress.iso_date, None)
        progress.last_commit_update = '2003-09-09 20:00'
        self.assertEqual(progress.iso_date, '2003-09-09T20:00')
