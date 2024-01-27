from django.test import TestCase
from django.contrib.auth.models import User
from journal.models import User, Group, GroupMembership

class GroupMembershipTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="@test_user", password='Password123', email="test@hotmail.com")
        self.group = Group.objects.create(name="Test Group")
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)

    def test_is_user_member(self):
        self.assertTrue(self.group.is_user_member(self.user))

    def test_is_non_member_false(self):
        another_user = User.objects.create(username="another_user", password='Password123', email="test3@hotmail.com")
        self.assertFalse(self.group.is_user_member(another_user))

    def test_group_name_is_invalid(self):
        self.group.name = "te3434234st"

    def test_group_name_is_valid(self):
        self.group.name = "test"

    def test_membership_attributes_valid(self):
        self.assertEqual(self.membership.user, self.user)
        self.assertEqual(self.membership.group, self.group)
        self.assertTrue(self.membership.is_owner)

    def test_member_cannot_be_added_twice(self):
        with self.assertRaises(Exception):
            GroupMembership.objects.create(user=self.user, group=self.group)