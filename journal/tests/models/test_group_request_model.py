from django.test import TestCase
from django.core.exceptions import ValidationError
from journal.models import Group, GroupRequest, User, GroupMembership

class GroupRequestTestCase(TestCase):
     """Unit tests for the Group Request model."""
     
    fixtures = ['journal/tests/fixtures/default_user.json',
                'journal/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.sender = User.objects.get(username='@janedoe')
        self.recipient = User.objects.get(username='@petrapickles')
        self.group = Group.objects.create(name='Test Group')
        self.ownership = GroupMembership.objects.create(user=self.sender, group=self.group, is_owner=True)
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=False)
        self.group_request = GroupRequest.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            group=self.group
        )

    def _assert_group_request_is_valid(self, group_request: GroupRequest, msg: str = None):
        try:
            group_request.full_clean()
        except ValidationError:
            self.fail(msg=msg)

    def _assert_group_request_is_invalid(self, group_request: GroupRequest, msg: str = None):
        with self.assertRaises(ValidationError, msg=msg):
            group_request.full_clean()

    def test_group_request_creation(self):
        self._assert_group_request_is_valid(self.group_request)

    def test_recipient_and_sender_different_users(self):
        self.group_request.recipient = self.sender
        self._assert_group_request_is_invalid(self.group_request)

    def test_sender_owner_of_group(self):
        self.group_request.sender = self.user
        self._assert_group_request_is_invalid(self.group_request)

    def test_valid_status_is_valid(self):
        for status, _ in GroupRequest.STATUS_CHOICES:
            self.group_request.status = status
            self._assert_group_request_is_valid(self.group_request, msg=f"{status} failed")

    def test_status_cannot_be_blank(self):
        self.group_request.status = ""
        self._assert_group_request_is_invalid(self.group_request)
        self._assert_group_request_is_invalid(self.group_request)

    def test_status_cannot_be_invalid(self):
        self.group_request.status = "Invalid Status"
        self._assert_group_request_is_invalid(self.group_request)
        self._assert_group_request_is_invalid(self.group_request)
