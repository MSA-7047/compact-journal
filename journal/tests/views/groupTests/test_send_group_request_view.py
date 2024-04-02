from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Group, GroupRequest, GroupMembership, Notification, User, FriendRequest

class SendGroupRequestViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email='test@example.com')
        self.recipient = User.objects.create(username='@testuser2', password='testpassword', email='test2@example.com')
        self.user.friends.add(self.recipient)
        self.group = Group.objects.create(name='Test Group')
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)

        print(self.user.friends.all())
        self.client = Client()

    def test_send_group_request(self):
        # Log in the user
        self.client.force_login(self.user)
        # Simulate sending a group request
        response = self.client.post(reverse('send_group_request', kwargs={'group_id': self.group.group_id}), {'recipient': self.recipient})

        
        # Check if the request was successful
        self.assertEqual(response.status_code, 200)  # Redirect to group dashboard
        self.assertTrue(GroupRequest.objects.filter(group=self.group).exists())
    
    def test_send_group_request_not_owner(self):
        other_user = User.objects.create(username='@testuser3', password='testpassword', email='test3@example.com')
        other_membership = GroupMembership.objects.create(user=self.recipient, group=self.group)
        self.user.friends.set([other_user])

        self.client.force_login(self.recipient)
        response = self.client.post(reverse('send_group_request', kwargs={'group_id': self.group.group_id}), data={'recipient': other_user}, follow=True)

        self.assertEqual(response.status_code, 200)  # Check if the user is redirected
        self.assertContains(response, "You are not authorized to send a group request")  # Check for error message content
    
    def test_accept_group_request(self):
        group_request = GroupRequest.objects.create(group=self.group, sender=self.user, recipient=self.recipient)
        self.client.force_login(self.recipient)
        response = self.client.post(reverse('accept_group_request', kwargs={'group_id': self.group.group_id}))

        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the group request is accepted

        # Check if GroupMembership is created for the user
        self.assertTrue(GroupMembership.objects.filter(user=self.recipient, group=self.group).exists())

        # Check if a notification is created for the sender
        self.assertTrue(Notification.objects.filter(user=self.user, message__contains=self.group.name).exists())
    
    def test_reject_group_request(self):
        group_request = GroupRequest.objects.create(group=self.group, sender=self.user, recipient=self.recipient)
        self.client.force_login(self.recipient)
        response = self.client.post(reverse('reject_group_request', kwargs={'group_id': self.group.group_id}))

        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the group request is accepted

        # Check if GroupMembership is created for the user
        self.assertFalse(GroupMembership.objects.filter(user=self.recipient, group=self.group).exists())

        # Check if a notification is created for the sender
        self.assertTrue(Notification.objects.filter(user=self.user, message__contains=self.group.name).exists())
    
    def test_delete_account_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('send_group_request', kwargs={'group_id': self.group.group_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'send_group_request.html')