from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import SendFriendRequestForm
from .models import FriendRequest

class FriendRequestTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

    def test_send_friend_request(self):
        self.client.login(username='user1', password='password1')
        url = reverse('send_request', kwargs={'user_id': self.user2.id})
        data = {'recipient': self.user2.id}
        
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('send_request', kwargs={'user_id': self.user2.id}))
        self.assertTrue(FriendRequest.objects.filter(recipient=self.user2, sender=self.user1, status='pending').exists())

    def test_accept_invitation(self):
        friend_request = FriendRequest.objects.create(recipient=self.user1, sender=self.user2)

        self.client.login(username='user1', password='password1')
        url = reverse('accept_invitation', kwargs={'friend_request_id': friend_request.id})
        
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('view_friend_requests'))
        friend_request.refresh_from_db()
        self.assertTrue(friend_request.is_accepted)
        self.assertEqual(friend_request.status, 'accepted')

    def test_reject_invitation(self):
        friend_request = FriendRequest.objects.create(recipient=self.user1, sender=self.user2)

        self.client.login(username='user1', password='password1')
        url = reverse('reject_invitation', kwargs={'friend_request_id': friend_request.id})
        
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('view_friend_requests'))
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'rejected')

    def test_delete_sent_request(self):
        friend_request = FriendRequest.objects.create(recipient=self.user2, sender=self.user1)

        self.client.login(username='user1', password='password1')
        url = reverse('delete_sent_request', kwargs={'friend_request_id': friend_request.id})
        
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('view_friend_requests'))
        self.assertFalse(FriendRequest.objects.filter(id=friend_request.id).exists())

    def test_remove_friend(self):
        self.user1.friends.add(self.user2)
        self.user2.friends.add(self.user1)

        self.client.login(username='user1', password='password1')
        url = reverse('remove_friend', kwargs={'user_id': self.user2.id})
        
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('friends'))
        self.assertFalse(self.user1.friends.filter(id=self.user2.id).exists())
        self.assertFalse(self.user2.friends.filter(id=self.user1.id).exists())