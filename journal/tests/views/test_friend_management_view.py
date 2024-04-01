from django.test import TestCase, Client
from django.urls import reverse
from journal.models import FriendRequest, Points, User

class FriendsViewTest(TestCase):

    fixtures = [
        'journal/tests/fixtures/default_user.json',
        'journal/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.friend = User.objects.get(username='@janedoe')
        self.client.login(username='@johndoe', password='Password123')

    def test_view_friend_requests(self):
        response = self.client.get(reverse('view_friend_requests'))
        self.assertEqual(response.status_code, 200)


    def test_view_friends(self):
        response = self.client.get(reverse('view_friends'))
        self.assertEqual(response.status_code, 200)


    def test_view_friends_profile(self):

        response = self.client.get(reverse('view_friends_profile', args=[self.friend.id]))
        self.assertEqual(response.status_code, 200)

    def test_remove_friend(self):
        self.user.friends.add(self.friend)
        self.assertEqual(self.user.friends.count(), 1)  # Assuming friend was added successfully
        response = self.client.post(reverse('remove_friend', args=[self.friend.id]))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after removing friend
        self.assertEqual(self.user.friends.count(), 0)  # Assuming friend was removed successfully

    def test_send_friend_request(self):
        response = self.client.post(reverse('send_request', args=[self.friend.id]), {'recipient': self.friend.id})
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(FriendRequest.objects.filter(sender=self.user, recipient=self.friend, status='pending').exists())

    def test_accept_invitation(self):
        friend_request = FriendRequest.objects.create(recipient=self.user, sender=self.friend)
        response = self.client.post(reverse('accept_friend_request', args=[friend_request.id]))
        self.assertEqual(response.status_code, 302)
        # Verify that the friend relationship is established
        self.assertTrue(self.friend.friends.filter(username='@johndoe').exists())
        self.assertTrue(self.user.friends.filter(username='@janedoe').exists())

        friend_request.refresh_from_db()
        self.assertTrue(friend_request.is_accepted)
        self.assertEqual(friend_request.status, 'accepted')

    def test_reject_invitation(self):
        friend_request = FriendRequest.objects.create(recipient=self.user, sender=self.friend)
        response = self.client.post(reverse('reject_friend_request', args=[friend_request.id]))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after rejecting request
        friend_request.refresh_from_db()
        self.assertFalse(friend_request.is_accepted)
        self.assertEqual(friend_request.status, 'rejected')

    def test_delete_sent_request(self):

        friend_request = FriendRequest.objects.create(recipient=self.friend, sender=self.user)
        response = self.client.post(reverse('delete_sent_request', args=[friend_request.id]))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after deleting request
        # Verify that the friend request is deleted
        self.assertFalse(FriendRequest.objects.filter(sender=self.user, recipient=self.friend).exists())