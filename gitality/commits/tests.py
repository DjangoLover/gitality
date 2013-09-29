from django.test import SimpleTestCase

from mock import Mock

from .models import CommitAuthor, Commit
from projects.models import Project


class CommitAuthorModelTest(SimpleTestCase):

    def test_update_from_commit(self):
        author = CommitAuthor(author_id=99)
        self.assertFalse(author.bio)
        self.assertFalse(author.following)
        self.assertFalse(author.followers)
        commit = Mock()
        commit.author.bio = 'Test'
        commit.author.following = 3
        commit.author.followers = 3
        author.update_from_commit(commit)
        self.assertEqual(author.bio, 'Test')
        self.assertEqual(author.following, 3)
        self.assertEqual(author.followers, 3)

    def test_create_from_real_commit(self):
        author = CommitAuthor.objects.create(
            author_id=99, login='asdad123')
        project = Project.objects.create(
            user_id=1, name='1', repo_url='http://google.com')
        self.assertEqual(Commit.objects.count(), 0)
        commit = Mock()
        commit.sha = '12312312312313'
        commit.additions = 0
        commit.deletions = 0
        commit.last_modified = '2012-09-09'
        Commit.objects.create_from_real_commit(commit, author, project)
        self.assertEqual(Commit.objects.count(), 1)
        Commit.objects.create_from_real_commit(commit, author, project)
        self.assertEqual(Commit.objects.count(), 1)
