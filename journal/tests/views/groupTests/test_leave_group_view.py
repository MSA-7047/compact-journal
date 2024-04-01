from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from journal.models import Group, GroupMembership, User

class LeaveGroupViewTest(TestCase):
    def setUp(self):
        # Create users
        self.owner_user = User.objects.create(username='@owner_user', password='ownerpass', email="owner@example.com")
        self.member_user = User.objects.create(username='@member_user', password='memberpass', email="member@example.com")

        # Create a group
        self.group = Group.objects.create(name='Test Group')

        # Create group memberships
        self.owner_membership = GroupMembership.objects.create(user=self.owner_user, group=self.group, is_owner=True)
        self.member_membership = GroupMembership.objects.create(user=self.member_user, group=self.group)

        # URL for the view
        self.url = reverse('leave_group', args=[self.group.group_id])

    def test_leave_group_member(self):
        """Test leaving the group as a member."""
        self.client.force_login(self.member_user)

        # Make the request
        response = self.client.post(self.url)

        # Check if the membership is deleted
        self.assertFalse(GroupMembership.objects.filter(user=self.member_user, group=self.group).exists())

        # Check if the group still exists
        self.assertTrue(Group.objects.filter(group_id=self.group.group_id).exists())

        # Check if redirected to home
        self.assertRedirects(response, reverse('dashboard'))

    def test_leave_group_owner_select_new_owner(self):
        """Test leaving the group as an owner and selecting a new owner."""
        self.client.force_login(self.owner_user)

        # Make the request with POST data for selecting a new owner
        response = self.client.post(self.url, {'new_owner': self.member_user.id})

        # Check if the ownership is transferred
        self.assertTrue(GroupMembership.objects.filter(group=self.group, user=self.member_user, is_owner=True).exists())

        # Check if redirected to home
        self.assertRedirects(response, reverse('home'))

    def test_leave_group_owner_no_new_owner(self):
        """Test leaving the group as an owner without selecting a new owner."""
        self.client.force_login(self.owner_user)

        # Make the request without POST data for selecting a new owner
        response = self.client.post(self.url)

        # Check if the appropriate message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertIn("You must select a new owner", str(messages[0]))

        # Check if the group still exists
        self.assertTrue(Group.objects.filter(id=self.group.group_id).exists())

        # Check if not redirected to home
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'select_new_owner.html')
    
    def test_owner_last_to_leave_group(self):
        self.member_membership.delete()
        self.client.force_login(self.owner_user)
        
        response = self.client.post(self.url)

        self.assertFalse(Group.objects.filter(group_id=self.group.group_id).exists())