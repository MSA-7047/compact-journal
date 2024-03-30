"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from journal.models import User
from journal.models import FriendRequest

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""
    fixtures = ['journal/tests/fixtures/default_user.json',
                'journal/tests/fixtures/other_users.json']
    
    def setUp(self):
        self.user = User.objects.get(username ="@johndoe")

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = User.objects.create_user(username='@testuser2', email='testuser2@example.org', password='Password123')
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'testuser'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.user.username = '@test!user'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user.username = '@te'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.user.username = '@testuser2'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user.username = '@@testuser'
        self._assert_user_is_invalid()

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'testuser.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'testuser@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'testuser@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'testuser@@example.org'
        self._assert_user_is_invalid()

    def test_full_name_must_be_correct(self):
        full_name = self.user.full_name()
        self.assertEqual(full_name, "Default User")

    def test_mini_gravatar(self):
        mini_gravatar_url = self.user.mini_gravatar()
        self.assertEqual(mini_gravatar_url, self.user.mini_gravatar())
        
    def test_send_friend_request(self):
        # Call send_friend_request method
        recipient = User.objects.get(username='@janedoe')
        invitation = self.user.send_friend_request(user=recipient)

        # Assert that a FriendRequest object is created or retrieved correctly
        self.assertIsInstance(invitation, FriendRequest)
        self.assertEqual(invitation.sender, self.user)
        self.assertEqual(invitation.recipient, recipient)

    def test_accept_request(self):
        # Create a friend request from another user to self.user
        sender = User.objects.get(username='@janedoe')
        friend_request = FriendRequest.objects.create(sender=sender, recipient=self.user)

        # Accept the friend request
        self.user.accept_request(user=sender)

        # Check if the sender is added to the user's friends list
        self.assertTrue(self.user.friends.filter(pk=sender.pk).exists())

        # Check if the friend request status is 'Accepted'
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'Accepted')

    def test_reject_request(self):
        # Create a friend request from another user to self.user
        sender = User.objects.get(username='@janedoe')
        friend_request = FriendRequest.objects.create(sender=sender, recipient=self.user)

        # Accept the friend request
        self.user.reject_request(user=sender)

        # Check if the sender is added to the user's friends list
        self.assertFalse(self.user.friends.filter(pk=sender.pk).exists())

        # Check if the friend request status is 'Accepted'
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'Rejected')

    def test_accept_nonexistant_request(self):
        sender = User.objects.get(username='@janedoe')
        self.assertFalse(self.user.accept_request(user=sender))

    def test_reject_nonexistant_request(self):
        sender = User.objects.get(username='@janedoe')
        self.assertFalse(self.user.reject_request(user=sender))

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except ValidationError:
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
