from django.test import TestCase

from mock import patch

from achievements.models import Achievement
from progresses.models import ProjectProgress
from projects.factories import ProjectFactory


class CommonProgressModelTest(TestCase):

    def test_project_progress_dirty_fields(self):
        project = ProjectFactory.create()
        self.assertEqual(project.progress.commit_count, 0)
        self.assertDictEqual(
            project.progress.get_dirty_fields_with_new_values(),
            {}
        )
        project.progress.commit_count += 1
        self.assertDictEqual(
            project.progress.get_dirty_fields_with_new_values(),
            {'commit_count': 1}
        )

    @patch('progresses.models.progress_state_changed.send')
    def test_progress_state_changed_signal_sent(self, send_patched):
        project = ProjectFactory.create()
        project.progress.save()
        self.assertFalse(send_patched.called)
        project.progress.commit_count += 1
        project.progress.save()
        self.assertTrue(send_patched.called)
        send_patched.assert_called_once_with(
            ProjectProgress,
            entity_type=Achievement.PROJECT,
            entity=project,
            dirty_fields={'commit_count': 1})
