from django.test import TestCase
from django.core.exceptions import ValidationError
from journal.models import Group, GroupRequest, User

class GroupRequestTestCase(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json',
                'journal/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.sender = User.objects.get(username='@janedoe')
        self.recipient = User.objects.get(username='@petrapickles')
        self.group = Group.objects.create(name='Test Group')
        self.group_request = GroupRequest.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            group=self.group
        )

    def test_group_request_creation(self):
        self.assertEqual(self.group_request.sender, self.sender)
        self.assertEqual(self.group_request.recipient, self.recipient)
        self.assertEqual(self.group_request.group, self.group)
        self.assertEqual(self.group_request.status, 'Pending')

    def test_recipient_and_sender_different_users(self):
        # Attempt to create a group request with the same sender and recipient
        with self.assertRaises(ValidationError):
            request = GroupRequest.objects.create(
                sender=self.sender,
                recipient=self.sender,
                group=self.group
            )
            request.clean()

    def test_sender_owner_of_group(self):
        # Attempt to create a group request where the sender is not the owner of the group
        with self.assertRaises(ValidationError):
            request = GroupRequest.objects.create(
                sender=self.user,  # User is not the owner of the group
                recipient=self.recipient,
                group=self.group
            )
            request.clean()