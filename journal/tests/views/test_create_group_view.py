from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import GroupForm
from .models import Group

class CreateGroupViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_group_successful(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('create_group')
        data = {
            'name': 'Test Group',
            'description': 'This is a test group',
            # Include any other required fields from your GroupForm
        }

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('groups'))
        self.assertTrue(Group.objects.filter(name='Test Group', creator=self.user).exists())