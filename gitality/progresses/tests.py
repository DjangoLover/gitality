from django.test import TestCase

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
