from sqlite3 import IntegrityError as SqIntegrityError
from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from journal.models import Group, GroupMembership, User
from django.utils import timezone


class GroupMembershipModelTest(TestCase):
    """Test Suite for GroupMembership Model Class"""

    fixtures = ['journal/tests/fixtures/default_user.json',
                'journal/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.user: User = User.objects.get(username='@johndoe')
        self.group: Group = Group.objects.create(name="Test Group")
        self.group_membership: GroupMembership = GroupMembership.objects.create(
            user=self.user,
            group=self.group,
            is_owner=True
        )

    def _assert_group_membership_is_valid(self, 
                                          membership: GroupMembership, 
                                          msg: str = None) -> None:
        try:
            membership.full_clean()
        except ValidationError:
            self.fail(msg=msg)

    def _assert_group_membership_is_invalid(self, 
                                            membership: GroupMembership,
                                            msg: str = None) -> None:
        with self.assertRaises((ValidationError, IntegrityError, SqIntegrityError), msg=msg):
            membership.full_clean()

    def test_group_membership_is_valid(self) -> None:
        self._assert_group_membership_is_valid(
            self.group_membership,
            "Default test failed"
        )

    def test_user_cannot_be_null(self) -> None:
        self.group_membership.user = None
        self._assert_group_membership_is_invalid(
            self.group_membership,
            "Membership has no user, which should register as invalid"
        )

    def test_group_cannot_be_null(self) -> None:
        self.group_membership.group = None
        self._assert_group_membership_is_invalid(
            self.group_membership,
            "Membership has no group, which should register as invalid"
        )

    def test_owner_field_cannot_be_null(self) -> None:
        self.group_membership.is_owner = None
        self._assert_group_membership_is_invalid(
            self.group_membership,
            "Membership has no type, which is invalid"
        )

    def test_membership_is_unique(self) -> None:
        with self.assertRaises(
                IntegrityError, 
                msg="Membership is no longer unique, and thus invalid"
            ):
            group_membership_2: GroupMembership = GroupMembership.objects.create(
                user=self.user,
                group=self.group,
                is_owner=True
            )

    



