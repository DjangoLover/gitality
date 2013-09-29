from django.test import SimpleTestCase

from mock import Mock

from .models import CommitAuthor


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
