from django.test import TestCase
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponseForbidden
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from journal.models import Group, GroupMembership, User

class RemovePlayerFromGroupViewTest(TestCase):
    def setUp(self):
        self.owner_user = User.objects.create(username='@owner', password='password123', email="example@example.com")
        self.player_user = User.objects.create(username='@player', password='password123', email="example@example2.com")
        self.group = Group.objects.create(name='Test Group')
        self.owner_membership = GroupMembership.objects.create(user=self.owner_user, group=self.group, is_owner=True)
        self.player_membership = GroupMembership.objects.create(user=self.player_user, group=self.group)
        self.url = reverse('remove_player_from_group', args=[self.group.group_id, self.player_user.id])

    def test_remove_player_as_owner(self):
        self.client.force_login(self.owner_user)
        response = self.client.post(self.url)

        # Check if the Membership has been deleted
        self.assertFalse(GroupMembership.objects.filter(user=self.player_user, group=self.group).exists())
        self.assertRedirects(response, reverse('group_dashboard', args=[self.group.group_id]))

    def test_remove_player_not_owner(self):
        """Test removing a player by a non-owner."""
        self.client.force_login(self.player_user)
        response = self.client.post(self.url)

        # Check if the response is Forbidden
        self.assertEqual(response.status_code, HttpResponseForbidden.status_code)
        # Check if the player is not removed from the group
        self.assertTrue(GroupMembership.objects.filter(user=self.player_user, group=self.group).exists())

    def test_not_remove_player_owner_remove_last_member(self):
        self.client.force_login(self.owner_user)
        self.client.post(self.url)

        # Check if the Group and the Membership has been deleted
        self.assertTrue(Group.objects.filter(group_id=self.group.group_id).exists())
        self.assertTrue(GroupMembership.objects.filter(group=self.group, user=self.owner_user, is_owner=True).exists())

    def test_remove_player_owner_cannot_remove_owner(self):
        self.client.force_login(self.owner_user)
        response = self.client.post(reverse('remove_player_from_group', args=[self.group.group_id, self.owner_user.id]))

        # Check if the owner is still a member of the group
        self.assertTrue(GroupMembership.objects.filter(user=self.owner_user, group=self.group, is_owner=True).exists())
        # Check if the appropriate message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "The owner cannot be removed from the group.")
    
    def test_remove_player_not_in_group(self):
        new_user = User.objects.create(username="@test17", password="TESTPASSWORD123", email="email@email.org")
        self.client.force_login(self.owner_user)

        response = self.client.post(reverse('remove_player_from_group', args=[self.group.group_id, new_user.id]))

        self.assertEqual(response.status_code, 404)
        # Check that the player is not removed from the group
        self.assertFalse(GroupMembership.objects.filter(user=new_user, group=self.group).exists())

