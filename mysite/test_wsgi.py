from django.test import TestCase
from .wsgi import project_name  # noqa: F403
import os


class TestWSGI(TestCase):
    def test_wsgi_settings_not_found(self):
        """Override project name, should fail"""
        project_name = "project_does_not_exist"
        base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        project_dir = os.path.basename(base_dir)
        self.assertNotEqual(project_dir, project_name)

    def test_wsgi_settings_exist(self):
        """Use project_name from .wsgi"""
        base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        project_dir = os.path.basename(base_dir)
        self.assertEqual(project_dir, project_name)  # noqa: F405
