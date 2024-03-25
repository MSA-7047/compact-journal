from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from journal.forms import GroupForm
from journal.models import Group, GroupMembership, User
from unittest.mock import patch, MagicMock

class EditGroupViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='@testuser', password='testpassword', email="example@example.com")
        self.group = Group.objects.create(name='Test Group')
        self.form = {'name': 'Test Group'}
        self.group_membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.client = Client()
        self.group.refresh_from_db()

    def test_edit_group_get_owner(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_group'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], GroupForm)

    def test_edit_group_get_not_owner(self):
        other_user = User.objects.create_user(username='@otheruser', password='testpassword', email="other@example.com")
        other_membership = self.group_membership = GroupMembership.objects.create(user=other_user, group=self.group, is_owner=False)
        self.client.force_login(other_user)
        response = self.client.get(reverse('edit_group', args=[self.group.group_id]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content.decode(), "You are not authorized to edit this group")

    def test_edit_group_get_not_member(self):
        other_user = User.objects.create_user(username='@otheruser', password='testpassword', email="other@example.com")
        self.client.force_login(other_user)
        response = self.client.get(reverse('edit_group', args=[self.group.group_id]))
        self.assertEqual(response.status_code, 404)

    def test_edit_group_post_valid(self):
        self.client.force_login(self.user)
        form_data = {'name': 'Updated Name'}
        response = self.client.post(reverse('edit_group', args=[self.group.group_id]), form_data)
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Group edited successfully'})
    
        # Refresh the group instance from the database
        self.group.refresh_from_db()
    
        # Check if the group name has been updated
        self.assertEqual(self.group.name, 'Updated Name')

    def test_edit_group_post_invalid(self):
        self.client.force_login(self.user)
        # Sending invalid form data
        form_data = {'name': ''}  # Empty name field
        response = self.client.post(reverse('edit_group', args=[self.group.group_id]), form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())

    def test_edit_group_not_logged_in(self):
        response = self.client.get(reverse('edit_group', args=[self.group.group_id]))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertIn('/log_in/', response.url)
