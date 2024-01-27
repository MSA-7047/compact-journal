from django.test import TestCase
from django.contrib.auth.models import User
from .models import Group, GroupMembership

class GroupMembershipTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(username="test_user")

        # Create a group
        self.group = Group.objects.create(name="Test Group")

        # Associate the user with the group through GroupMembership
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group)

    def test_is_user_member(self):
        # Test if the user is a member of the group
        self.assertTrue(self.group.is_user_member(self.user))

        # Test if another user is not a member of the group
        another_user = User.objects.create(username="another_user")
        self.assertFalse(self.group.is_user_member(another_user))
        