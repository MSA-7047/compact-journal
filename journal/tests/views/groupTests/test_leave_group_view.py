from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from journal.models import Group, GroupMembership, User

class LeaveGroupViewTest(TestCase):
    def setUp(self):
        self.owner_user = User.objects.create(username='@owner_user', password='ownerpass', email="owner@example.com")
        self.member_user = User.objects.create(username='@member_user', password='memberpass', email="member@example.com")
        self.group = Group.objects.create(name='Test Group')
        self.owner_membership = GroupMembership.objects.create(user=self.owner_user, group=self.group, is_owner=True)
        self.member_membership = GroupMembership.objects.create(user=self.member_user, group=self.group)
        self.url = reverse('leave_group', args=[self.group.group_id])

    def test_leave_group_member(self):
        self.client.force_login(self.member_user)
        response = self.client.post(self.url)

        # Check if the membership is deleted
        self.assertFalse(GroupMembership.objects.filter(user=self.member_user, group=self.group).exists())
        self.assertTrue(Group.objects.filter(group_id=self.group.group_id).exists())
        self.assertRedirects(response, reverse('dashboard'))

    def test_leave_group_owner_select_new_owner(self):
        self.client.force_login(self.owner_user)

        # Make the request with POST data for selecting a new owner
        response = self.client.post(self.url, {'new_owner': self.member_user})

        # Check if the ownership is transferred
        self.assertFalse(GroupMembership.objects.filter(group=self.group, user=self.member_user, is_owner=True).exists())
        self.assertRedirects(response,f'/groups/{self.group.group_id}/select-new-owner')