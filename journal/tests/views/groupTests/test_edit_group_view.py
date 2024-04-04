from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from journal.forms import GroupForm
from journal.models import Group, GroupMembership, User
from unittest.mock import patch, MagicMock

class EditGroupViewTest(TestCase):
    """Test suite for edit group view"""

    def setUp(self):
        self.user = User.objects.create_user(username='@testuser', password='testpassword', email="example@example.com")
        self.group = Group.objects.create(name='Test Group')
        self.group_membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.client = Client()

    def test_edit_group_owner(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': 'Updated Group Name'})

        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.group_id}))

        updated_group = Group.objects.get(group_id=self.group.group_id)
        self.assertEqual(updated_group.name, 'Updated Group Name')

    def test_edit_group_non_owner(self):
        other_user = User.objects.create(username='@other_user', password='test_password', email="email@gmail.com")
        GroupMembership.objects.create(user=other_user, group=self.group)

        self.client.force_login(other_user)
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': 'Attempted Update'})
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.group_id}))

        refreshed_group = Group.objects.get(group_id=self.group.group_id)
        self.assertEqual(refreshed_group.name, 'Test Group')

    def test_edit_group_unauthenticated_user(self):
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': 'Attempted Update'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/log_in/?next=/groups/{self.group.group_id}/edit')

    def test_edit_group_invalid_form(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': ''})
        self.assertEqual(response.status_code, 200)
        
        refreshed_group = Group.objects.get(group_id=self.group.group_id)
        self.assertEqual(refreshed_group.name, 'Test Group')

    def test_edit_group_long_name(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_group', kwargs={'group_id': self.group.group_id}), {'name': 'sadioaodiasjomdiasodisamodsamodissmaodamoda'})
        self.assertEqual(response.status_code, 200)  

        refreshed_group = Group.objects.get(group_id=self.group.group_id)
        self.assertEqual(refreshed_group.name, 'Test Group')
    
    def test_edit_group_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_group', kwargs={'group_id': self.group.group_id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_group.html')