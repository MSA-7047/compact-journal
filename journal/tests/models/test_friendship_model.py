from django.db import IntegrityError
from django.test import TestCase
from journal.models import Friendship, User
from django.core.exceptions import ValidationError

class FriendshipModelTest(TestCase):

    fixtures = [
        'journal/tests/fixtures/default_user.json',
        'journal/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user1 = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')

    def test_create_friendship(self):
        friendship = Friendship.objects.create(user=self.user1, friend=self.user2)
        self.assertEqual(friendship.user, self.user1)
        self.assertEqual(friendship.friend, self.user2)

    def test_unique_together_constraint(self):
        # Create a friendship
        friendship = Friendship.objects.create(user=self.user1, friend=self.user2)
        friendship.clean()
        # Try to create another friendship with the same user and friend
        with self.assertRaises(IntegrityError):
            Friendship.objects.create(user=self.user1, friend=self.user2)

    def test_clean_method(self):
        # Attempt to create a friendship with the same user and friend
        with self.assertRaises(ValidationError) as context:
            friendship = Friendship.objects.create(user=self.user1, friend=self.user1)
            friendship.clean()
        self.assertTrue('User and Friend cannot refer to the same user' in str(context.exception))