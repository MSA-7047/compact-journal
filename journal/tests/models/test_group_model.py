from django.test import TestCase
from django.contrib.auth.models import User
from journal.models import User, Group, GroupMembership

class GroupMembershipTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Test Group")
        self.user = User.objects.create(username="@test_user", password='Password123', email="test@hotmail.com")
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.user2 = User.objects.create(username="@test_user2", password='Password123', email="test2@hotmail.com")
        self.membership2 = GroupMembership.objects.create(user=self.user2, group=self.group)

    def test_is_user_member(self):
        self.assertTrue(self.group.is_user_member(self.user))

    def test_is_non_member_false(self):
        another_user = User.objects.create(username="@another_user", password='Password123', email="test3@hotmail.com")
        self.assertFalse(self.group.is_user_member(another_user))

    def test_membership_attributes_valid(self):
        self.assertEqual(self.membership.user, self.user)
        self.assertEqual(self.membership.group, self.group)
        self.assertTrue(self.membership.is_owner)
    
    def test_other_user_is_not_owner(self):
        self.assertFalse(self.membership2.is_owner, False)

    def test_same_user_cannot_be_added_twice(self):
        with self.assertRaises(Exception):
            GroupMembership.objects.create(user=self.user, group=self.group)