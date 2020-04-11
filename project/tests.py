from django.test import TestCase
from .models import Project, Field, Table
from django.contrib.auth import get_user_model
# Create your tests here.
User = get_user_model()

class TestProject(TestCase):
    def setUp(self):
        self.user = User.objects.create(
                username="Test User",
                email = "testuser@testmail.com",
            )
        self.user.set_password('somepassword')
    def test_create_project(self):
        project = Project.objects.create(
            name="Test Project",
            authentication = True,
            description = "A test project",
            owner = self.user
        )
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.authentication, True)
        self.assertEqual(project.description, "A test project")
        self.assertEqual(project.owner, self.user)
    
    def test_modify_project(self):
        project = Project.objects.create(
            name="Test Project",
            authentication = True,
            description = "A test project",
            owner = self.user
        )
        project.name = "New name"
        project.authentication = False
        project.description = "New description"
        
        self.assertEqual(project.name, "New name")
        self.assertEqual(project.authentication, False)
        self.assertEqual(project.description, "New description")
        self.assertEqual(project.owner, self.user)