from django.test import TestCase

from mock import patch

from achievements.models import Achievement
from progresses.models import ProjectProgress
from projects.factories import ProjectFactory


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
