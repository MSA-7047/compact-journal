from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from journal.models import FriendRequest, User


class ViewFriendRequestsTestCase(TestCase):

    fixtures = [
        'journal/tests/fixtures/default_user.json',
        'journal/tests/fixtures/other_users.json'
    ]



    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.friend = User.objects.get(username='@janedoe')


    def test_view_friend_requests(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('view_friend_requests'))
        self.assertEqual(response.status_code, 200)

    def test_send_friend_request(self):
        self.client.login(username='user1', password='password')
        user_id = 1  # ID of the user to send the friend request to
        response = self.client.post(reverse('send_request', kwargs={'user_id': user_id}))
        self.assertEqual(response.status_code, 302)   # Check if the request is redirected


    def test_accept_invitation(self):
        friend_request = FriendRequest.objects.create(sender=self.user, recipient=self.user)
        self.client.force_login(self.user)
        response = self.client.get(reverse('accept_friend_request', kwargs={'friend_request_id': friend_request.id}))
        self.assertEqual(response.status_code, 302)  # Check if the request is redirected

    # def test_reject_invitation(self):
    #     friend_request = FriendRequest.objects.create(sender=self.user, recipient=self.friend)
    #     self.client.force_login(self.user)
    #     response = self.client.get(reverse('reject_friend_request', kwargs={'friend_request_id': friend_request.id}))
    #     self.assertEqual(response.status_code, 302)  # Check if the request is redirected

    def test_delete_sent_request(self):
        friend_request = FriendRequest.objects.create(sender=self.user, recipient=self.friend)
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_sent_request', kwargs={'friend_request_id': friend_request.id}))
        self.assertEqual(response.status_code, 302)  # Check if the request is redirected

    def test_remove_friend(self):
        self.user.friends.add(self.friend)
        self.client.force_login(self.user)
        response = self.client.get(reverse('remove_friend', kwargs={'user_id': self.friend.id}))
        self.assertEqual(response.status_code, 302)  # Check if the request is redirected
