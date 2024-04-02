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

        self.client = Client()

    def test_send_group_request(self):
        # Log in the user
        self.client.force_login(self.user)
        # Simulate sending a group request
        response = self.client.post(reverse('send_group_request', kwargs={'group_id': self.group.group_id}), {'recipient': self.recipient.id})

        
        # Check if the request was successful
        self.assertEqual(response.status_code, 302)  # Redirect to group dashboard
        self.assertTrue(GroupRequest.objects.filter(group=self.group, recipient=self.recipient, sender=self.user).exists())
    
    def test_send_group_request_not_owner(self):
        other_user = User.objects.create(username='@testuser3', password='testpassword', email='test3@example.com')
        other_membership = GroupMembership.objects.create(user=self.recipient, group=self.group)
        self.user.friends.set([other_user])

        self.client.force_login(self.recipient)
        response = self.client.post(reverse('send_group_request', kwargs={'group_id': self.group.group_id}), data={'recipient': other_user.id}, follow=True)

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
    
    def test_send_request_already_existing_request(self):
        other_membership = GroupRequest.objects.create(recipient=self.recipient, group=self.group, sender=self.user)

        self.client.force_login(self.user)
        response = self.client.post(reverse('send_group_request', kwargs={'group_id': self.group.group_id}), data={'recipient': self.recipient.id})

        self.assertEqual(response.status_code, 200)  # Check if the user is redirected
        self.assertContains(response, f"{self.recipient} has already been invited.")  # Check for error message content

    def test_send_request_already_existing_member(self):
        other_membership = GroupMembership.objects.create(user=self.recipient, group=self.group)

        self.client.force_login(self.user)
        response = self.client.post(reverse('send_group_request', kwargs={'group_id': self.group.group_id}), data={'recipient': self.recipient.id})

        self.assertEqual(response.status_code, 200)  # Check if the user is redirected
        self.assertContains(response, f"{self.recipient} is already a member.")  # Check for error message content
    
    def test_send_request_invalid_form(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('send_group_request', kwargs={'group_id': self.group.group_id}), data={'recipient': "User3"})

        self.assertEqual(response.status_code, 200)  # Check if the user is redirected
    
    def test_send_group_request_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('send_group_request', kwargs={'group_id': self.group.group_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'send_group_request.html')
    