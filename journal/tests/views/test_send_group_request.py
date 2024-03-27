from django.test import TestCase
from django.urls import reverse
from journal.models import User, Group, GroupRequest, GroupMembership

class SendGroupRequestViewTest(TestCase):
    def setUp(self):
        # Create users
        self.sender_user = User.objects.create_user(username='sender', email='sender@example.com', password='senderpass')
        self.recipient_user = User.objects.create_user(username='recipient', email='recipient@example.com', password='recipientpass')

        self.sender_user.send_friend_request(self.recipient_user)
        self.recipient_user.accept_request(self.sender_user)

        # Create a group
        self.group = Group.objects.create(name='Test Group')

        self.sender_membership = GroupMembership.objects.create(user=self.sender_user, group=self.group, is_owner=True)

    def test_send_group_request(self):
        # Log in as sender user
        self.client.force_login(self.sender_user)

        # Make a POST request to send a group request
        response = self.client.post(reverse('send_group_request', args=[self.group.group_id]), {'recipient': self.recipient_user.pk})

        # Check if the group request is created
        self.assertEqual(GroupRequest.objects.filter(sender=self.sender_user, recipient=self.recipient_user, group=self.group).count(), 1)

        # Check if the user is redirected to the group dashboard
        self.assertRedirects(response, reverse('group_dashboard', args=[self.group.group_id]))

    def test_send_group_request_invalid(self):
        # Log in as sender user
        self.client.force_login(self.sender_user)

        # Create a group request to the same recipient and group
        GroupRequest.objects.create(sender=self.sender_user, recipient=self.recipient_user, group=self.group)

        # Make a POST request to send another group request to the same recipient and group
        response = self.client.post(reverse('send_group_request', args=[self.group.group_id]), {'recipient': self.recipient_user.id})

        # Check if the form has errors
        self.assertFormError(response, 'form', 'recipient', 'This user has already been sent an invitation.')
