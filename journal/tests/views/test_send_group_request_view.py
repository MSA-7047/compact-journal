from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Group, GroupRequest, GroupMembership, Notification, User, FriendRequest

class SendGroupRequestViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email='test@example.com')
        self.recipient = User.objects.create(username='@testuser2', password='testpassword', email='test2@example.com')
        self.user.friends.set([self.recipient])
        self.group = Group.objects.create(name='Test Group')
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)

        self.client = Client()

    def test_send_group_request(self):
        # Log in the user
        self.client.force_login(self.user)

        # Simulate sending a group request
        response = self.client.post(reverse('send_group_request', kwargs={'group_id': self.group.group_id}), data={'recipient': self.recipient})

        # Check if the request was successful
        self.assertEqual(response.status_code, 200)  # Redirect to group dashboard
    
    def test_send_group_request_not_owner(self):
        other_user = User.objects.create(username='@testuser3', password='testpassword', email='test3@example.com')
        other_membership = GroupMembership.objects.create(user=self.recipient, group=self.group)
        self.user.friends.set([other_user])

        self.client.force_login(self.recipient)
        response = self.client.post(reverse('send_group_request', kwargs={'group_id': self.group.group_id}), data={'recipient': other_user}, follow=True)

        self.assertEqual(response.status_code, 200)  # Check if the user is redirected
        self.assertContains(response, "You are not authorized to send a group request")  # Check for error message content

