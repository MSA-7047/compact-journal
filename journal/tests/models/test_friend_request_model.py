from django.test import TestCase
from journal.models import FriendRequest, User
from django.core.exceptions import ValidationError


class FriendRequestModelTest(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json',
                'journal/tests/fixtures/other_users.json']
    
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.friend_request = FriendRequest.objects.create(
            recipient=self.user,
            sender=self.user2,
            status='Pending',
            is_accepted=False
        )

    def _assert_friend_request_is_valid(self, friend_request: FriendRequest, msg: str = None) -> None:
        try:
            friend_request.full_clean()
        except ValidationError:
            self.fail(msg=msg)

    def _assert_friend_request_is_invalid(self, friend_request: FriendRequest, msg: str = None) -> None:
        with self.assertRaises(ValidationError, msg=msg):
            friend_request.full_clean()

    def test_create_friend_request(self):
        self._assert_friend_request_is_valid(self.friend_request)

    def test_valid_status_is_valid(self):
        for status, _ in FriendRequest.STATUS_CHOICES:
            self.friend_request.status = status
            self._assert_friend_request_is_valid(self.friend_request, msg=f"{status} failed")

    def test_status_cannot_be_blank(self):
        self.friend_request.status = ""
        self._assert_friend_request_is_invalid(self.friend_request)

    def test_status_cannot_be_invalid(self):
        self.friend_request.status = "Invalid Status"
        self._assert_friend_request_is_invalid(self.friend_request)

    def test_accepted_status_defaults_to_false(self):
        friend_request = FriendRequest.objects.create(
            recipient=self.user,
            sender=self.user2,
            status='Pending',
        )

        self.assertFalse(friend_request.is_accepted)

    def test_str_method(self):
        friend_request = FriendRequest.objects.create(
            recipient=self.user,
            sender=self.user2,
            status='Pending',
            is_accepted=False
        )

        self.assertEqual(str(friend_request), f"Friend request from {self.user2} to {self.user}")
