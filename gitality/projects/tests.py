from django.test import SimpleTestCase

from .forms import ProjectForm


class ProjectFormTest(SimpleTestCase):

    def test_repo_url_validation(self):

        # Valid repo url
        post_data = {
            'name': 'Gitality',
            'repo_url': 'https://github.com/dmrz/gitality.git'
        }
        form = ProjectForm(post_data)
        self.assertTrue(form.is_valid())

        # Check that .git part is truncated
        self.assertEqual(form.cleaned_data['repo_url'], post_data['repo_url'].replace('.git', ''))

        # Invalid repo url
        post_data['repo_url'] = post_data['repo_url'].replace('github', 'othersite')
        form = ProjectForm(post_data)
        self.assertFalse(form.is_valid())

        self.assertIn('repo_url', form.errors)
