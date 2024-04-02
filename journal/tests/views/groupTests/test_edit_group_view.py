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
        self.group_membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.client = Client()

    def test_edit_group_owner(self):
        """Test editing a group by its owner."""
        self.client.force_login(self.user)
        new_group_name = 'Updated Group Name'
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': new_group_name})
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.group_id}))
        # Refresh the group instance from the database to get the latest changes
        updated_group = Group.objects.get(group_id=self.group.group_id)
        self.assertEqual(updated_group.name, new_group_name)

    def test_edit_group_non_owner(self):
        """Test editing a group by a non-owner."""
        # Create another user who is not the owner of the group
        other_user = User.objects.create(username='@other_user', password='test_password', email="email@gmail.com")
        other_membership = GroupMembership.objects.create(user=other_user, group=self.group)
        self.client.force_login(other_user)
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': 'Attempted Update'})
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.group_id}))
        # Refresh the group instance from the database to ensure the name remains unchanged
        refreshed_group = Group.objects.get(group_id=self.group.group_id)
        self.assertEqual(refreshed_group.name, 'Test Group')

    def test_edit_group_unauthenticated(self):
        """Test editing a group by an unauthenticated user."""
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': 'Attempted Update'})
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

    def test_edit_group_invalid_form(self):
        """Test editing a group with invalid form data."""
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': ''})
        self.assertEqual(response.status_code, 200)  # Should stay on the edit page
        # Ensure the group name remains unchanged
        refreshed_group = Group.objects.get(group_id=self.group.group_id)
        self.assertEqual(refreshed_group.name, 'Test Group')

    def test_edit_group_long_name(self):
        """Test editing a group with invalid form data."""
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': 'sadioaodiasjomdiasodisamodsamodissmaodamoda'})
        self.assertEqual(response.status_code, 200)  # Should stay on the edit page
        # Ensure the group name remains unchanged
        refreshed_group = Group.objects.get(group_id=self.group.group_id)
        self.assertEqual(refreshed_group.name, 'Test Group')
    
    def test_edit_group_GET(self):
        self.client.force_login(self.user)
        
        response = self.client.get(reverse('edit_group', kwargs={'group_id': self.group.group_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_group.html')