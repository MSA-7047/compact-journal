from django.test import TestCase
from django.urls import reverse
from journal.forms import GroupForm
from journal.models import Group, GroupMembership, User
from django.contrib.messages import get_messages

class CreateGroupViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='@testuser', password='testpassword', email="example@example.org")

    def test_create_group_successful(self):
        self.client.login(username='@testuser', password='testpassword')
        url = reverse('create_group')
        data = {'name': 'Test Group', 'description': 'This is a test group'}
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('groups'))
        self.assertTrue(Group.objects.filter(name='Test Group').exists())
        self.assertTrue(GroupMembership.objects.filter(group=Group.objects.filter(name='Test Group').exists(), user=self.user, is_owner=True).exists())
    
    def test_create_group_get(self):
        self.client.login(username='@testuser', password='testpassword')
        response = self.client.get(reverse('create_group'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_group.html')
        self.assertIsInstance(response.context['form'], GroupForm)

    def test_create_group_unauthenticated_access(self):
        url = reverse('create_group')
        response = self.client.get(url)
        self.assertRedirects(response, '/log_in/?next=/create_group/')

    def test_create_group_invalid_form_data(self):
        self.client.login(username='@testuser', password='testpassword')
        url = reverse('create_group')
        data = {'name': ''}  # Invalid data
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Form should not redirect
        self.assertFormError(response, 'form', 'name', 'This field is required.')
    
    def test_multiple_group_create_gives_correct_response(self):

        self.client.login(username='@testuser', password='testpassword')
        url = reverse('create_group')
        data = {'name': 'Test Group', 'description': 'This is a test group'}
        self.client.post(url, data)

        data2 = {'name': 'Second Test Group', 'description': 'This is a Second test group'}
        response = self.client.post(url, data2)
        messages = list(get_messages(response.wsgi_request))
        found_message = ""
        expected_message = "New group created! However, you must wait before getting points again."

        for message in messages:
            if str(message) == expected_message:
                found_message = str(message)
                break

        self.assertTrue(found_message, expected_message)
