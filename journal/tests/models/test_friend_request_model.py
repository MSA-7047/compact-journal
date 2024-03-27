from django.test import TestCase
from journal.models import FriendRequest, User
from django.core.exceptions import ValidationError


class FriendRequestModelTest(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json',
                'journal/tests/fixtures/other_users.json']
    
    def setUp(self):
        # Create users for testing
        self.user = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')

    def test_create_friend_request(self):
        # Create a FriendRequest instance
        friend_request = FriendRequest.objects.create(
            recipient=self.user,
            sender=self.user2,
            status='Pending',
            is_accepted=False
        )

        # Check if the friend_request is created successfully
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertEqual(friend_request.recipient, self.user)
        self.assertEqual(friend_request.sender, self.user2)
        self.assertEqual(friend_request.status, 'Pending')
        self.assertFalse(friend_request.is_accepted)

    def test_update_friend_request_status(self):
        # Create a FriendRequest instance
        friend_request = FriendRequest.objects.create(
            recipient=self.user,
            sender=self.user2,
            status='Pending',
            is_accepted=False
        )

        # Update the status of the friend_request
        friend_request.status = 'Accepted'
        friend_request.save()

        # Check if the status is updated successfully
        updated_friend_request = FriendRequest.objects.get(pk=friend_request.pk)
        self.assertEqual(updated_friend_request.status, 'Accepted')

    def test_accepted_status_defaults_to_false(self):
        # Create a FriendRequest without explicitly setting is_accepted
        friend_request = FriendRequest.objects.create(
            recipient=self.user,
            sender=self.user2,
            status='Pending',
        )

        # Check if is_accepted defaults to False
        self.assertFalse(friend_request.is_accepted)
    

    def test_str_method(self):
        # Create a FriendRequest instance
        friend_request = FriendRequest.objects.create(
            recipient=self.user,
            sender=self.user2,
            status='Pending',
            is_accepted=False
        )

        # Check if the __str__ method returns the expected string representation
        self.assertEqual(str(friend_request), f"Friend request from {self.user2} to {self.user}")
