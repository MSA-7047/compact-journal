from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from journal.models import User, Group, GroupMembership
from django.core.exceptions import ValidationError

class GroupMembershipTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Test Group", description="Test Description")
        self.user = User.objects.create(username="@test_user", password='Password123', email="test@hotmail.com")
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.user2 = User.objects.create(username="@test_user2", password='Password123', email="test2@hotmail.com")
        self.membership2 = GroupMembership.objects.create(user=self.user2, group=self.group)

    def _assert_group_is_valid(self, group: Group, msg: str = None) -> None:
        try:
            group.full_clean()
        except ValidationError:
            self.fail(msg=msg)
    
    def _assert_group_is_invalid(self, group: Group, msg: str = None) -> None:
        with self.assertRaises(ValidationError, msg=msg):
            group.full_clean()

    def test_group_is_valid(self):
        self._assert_group_is_valid(self.group)

    def test_group_name_accepted_with_30_characters(self):
        self.group.name = 'x' * 30
        self._assert_group_is_valid(self.group)

    def test_group_name_rejected_with_more_than_30_characters(self):
        self.group.name = 'x' * 31
        self._assert_group_is_invalid(self.group)

    def test_group_description_accepted_with_50_characters(self):
        self.group.description = 'x' * 50
        self._assert_group_is_valid(self.group)

    def test_group_description_rejected_with_more_than_30_characters(self):
        self.group.description = 'x' * 51
        self._assert_group_is_invalid(self.group)
    
    def test_is_user_member(self):
        self.assertTrue(self.group.is_user_member(self.user))

    def test_is_non_member_false(self):
        another_user = User.objects.create(username="@another_user", password='Password123', email="test3@hotmail.com")
        self.assertFalse(self.group.is_user_member(another_user))

    def test_group_date_created(self):
        self.assertIsInstance(self.group.date_created, datetime)
    
    def test_str_valid(self):
        self.assertEqual(self.group.name, str(self.group))
