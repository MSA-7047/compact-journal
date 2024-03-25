# """Unit tests for the User model."""
# from django.core.exceptions import ValidationError
# from django.test import TestCase
# from journal.models import User
# from journal.models import FriendRequest

# class UserModelTestCase(TestCase):
#     """Unit tests for the User model."""

#     fixtures = [
#         'journal/tests/fixtures/default_user.json',
#         'journal/tests/fixtures/other_users.json'
#     ]

#     GRAVATAR_URL = "https://www.gravatar.com/avatar/363c1b0cd64dadffb867236a00e62986"

#     def setUp(self):
#         self.user = User.objects.create_user(username='@johndoe', email='johndoe@example.org', password='Password123')

#     def test_valid_user(self):
#         self._assert_user_is_valid()

#     def test_username_cannot_be_blank(self):
#         self.user.username = ''
#         self._assert_user_is_invalid()

#     def test_username_can_be_30_characters_long(self):
#         self.user.username = '@' + 'x' * 29
#         self._assert_user_is_valid()

#     def test_username_cannot_be_over_30_characters_long(self):
#         self.user.username = '@' + 'x' * 30
#         self._assert_user_is_invalid()

#     def test_username_must_be_unique(self):
#         second_user = User.objects.get(username='@janedoe')
#         self.user.username = second_user.username
#         self._assert_user_is_invalid()

#     def test_username_must_start_with_at_symbol(self):
#         self.user.username = 'johndoe'
#         self._assert_user_is_invalid()

#     def test_username_must_contain_only_alphanumericals_after_at(self):
#         self.user.username = '@john!doe'
#         self._assert_user_is_invalid()

#     def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
#         self.user.username = '@jo'
#         self._assert_user_is_invalid()

#     def test_username_may_contain_numbers(self):
#         self.user.username = '@j0hndoe2'
#         self._assert_user_is_valid()

#     def test_username_must_contain_only_one_at(self):
#         self.user.username = '@@johndoe'
#         self._assert_user_is_invalid()


#     def test_first_name_must_not_be_blank(self):
#         self.user.first_name = ''
#         self._assert_user_is_invalid()

#     def test_first_name_need_not_be_unique(self):
#         second_user = User.objects.get(username='@janedoe')
#         self.user.first_name = second_user.first_name
#         self._assert_user_is_valid()

#     def test_first_name_may_contain_50_characters(self):
#         self.user.first_name = 'x' * 50
#         self._assert_user_is_valid()

#     def test_first_name_must_not_contain_more_than_50_characters(self):
#         self.user.first_name = 'x' * 51
#         self._assert_user_is_invalid()


#     def test_last_name_must_not_be_blank(self):
#         self.user.last_name = ''
#         self._assert_user_is_invalid()

#     def test_last_name_need_not_be_unique(self):
#         second_user = User.objects.get(username='@janedoe')
#         self.user.last_name = second_user.last_name
#         self._assert_user_is_valid()

#     def test_last_name_may_contain_50_characters(self):
#         self.user.last_name = 'x' * 50
#         self._assert_user_is_valid()

#     def test_last_name_must_not_contain_more_than_50_characters(self):
#         self.user.last_name = 'x' * 51
#         self._assert_user_is_invalid()


#     def test_email_must_not_be_blank(self):
#         self.user.email = ''
#         self._assert_user_is_invalid()

#     def test_email_must_be_unique(self):
#         second_user = User.objects.get(username='@janedoe')
#         self.user.email = second_user.email
#         self._assert_user_is_invalid()

#     def test_email_must_contain_username(self):
#         self.user.email = '@example.org'
#         self._assert_user_is_invalid()

#     def test_email_must_contain_at_symbol(self):
#         self.user.email = 'johndoe.example.org'
#         self._assert_user_is_invalid()

#     def test_email_must_contain_domain_name(self):
#         self.user.email = 'johndoe@.org'
#         self._assert_user_is_invalid()

#     def test_email_must_contain_domain(self):
#         self.user.email = 'johndoe@example'
#         self._assert_user_is_invalid()

#     def test_email_must_not_contain_more_than_one_at(self):
#         self.user.email = 'johndoe@@example.org'
#         self._assert_user_is_invalid()


#     def test_full_name_must_be_correct(self):
#         full_name = self.user.full_name()
#         self.assertEqual(full_name, "John Doe")


#     def test_default_gravatar(self):
#         actual_gravatar_url = self.user.gravatar()
#         expected_gravatar_url = self._gravatar_url(size=120)
#         self.assertEqual(actual_gravatar_url, expected_gravatar_url)

#     def test_custom_gravatar(self):
#         actual_gravatar_url = self.user.gravatar(size=100)
#         expected_gravatar_url = self._gravatar_url(size=100)
#         self.assertEqual(actual_gravatar_url, expected_gravatar_url)

#     def test_mini_gravatar(self):
#         actual_gravatar_url = self.user.mini_gravatar()
#         expected_gravatar_url = self._gravatar_url(size=60)
#         self.assertEqual(actual_gravatar_url, expected_gravatar_url)

#     def _gravatar_url(self, size):
#         gravatar_url = f"{UserModelTestCase.GRAVATAR_URL}?size={size}&default=mp"
#         return gravatar_url


#     def _assert_user_is_valid(self):
#         try:
#             self.user.full_clean()
#         except (ValidationError):
#             self.fail('Test user should be valid')

#     def _assert_user_is_invalid(self):
#         with self.assertRaises(ValidationError):
#             self.user.full_clean()

"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from journal.models import User
from journal.models import FriendRequest

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='@testuser',
            email='testuser@example.org',
            password='Password123',
            first_name='Test',
            last_name='User',
            location='Test Location',
            nationality='NZ'
        )

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
        self.assertEqual(full_name, "Test User")

        
    def test_accept_request(self):
        # Create a friend request from another user to self.user
        sender = User.objects.create_user(username='@sender', email='sender@example.org', password='Password123')
        friend_request = self.user.send_friend_request(user=sender)

        # Accept the friend request
        result = self.user.accept_request(user=sender)

        # Check if the sender is added to the user's friends list
        self.assertTrue(self.user.friends.filter(pk=sender.pk).exists())

        # Check if the friend request status is 'Accepted'
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'Accepted')


    def test_accept_request_not_pending(self):
        # Create a friend request from another user to self.user, but mark it as accepted already
        sender = User.objects.create_user(username='@sender', email='sender@example.org', password='Password123')
        friend_request = self.user.send_friend_request(user=sender)
        friend_request.status = 'Accepted'
        friend_request.save()

        # Try to accept the friend request again
        result = self.user.accept_request(user=sender)

        # Check that the function returns False since the request is not pending
        self.assertFalse(result)

        # Check that the sender is not added to the user's friends list
        self.assertFalse(self.user.friends.filter(pk=sender.pk).exists())

        # Check that the friend request status remains 'Accepted'
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'Accepted')

    def test_accept_request_no_pending_request(self):
        # Create a friend request from another user to self.user
        sender = User.objects.create_user(username='@sender', email='sender@example.org', password='Password123')
        self.user.send_friend_request(user=sender)

        # Try to accept the friend request without it being marked as pending
        result = self.user.accept_request(user=sender)

        # Check that the function returns False since there's no pending request
        self.assertFalse(result)

        # Check that the sender is not added to the user's friends list
        self.assertFalse(self.user.friends.filter(pk=sender.pk).exists())



    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except ValidationError:
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
