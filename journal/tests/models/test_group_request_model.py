from django.contrib.auth import get_user_model
from django.test import TestCase
from journal.models import Group, GroupRequest, User

class GroupRequestTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='@sender', password='Password123', email='example@example.com')
        self.recipient = User.objects.create_user(username='@recipient', password='Password123', email='example2@example.com')
        self.group = Group.objects.create(name='Test')

    def test_group_request_creation(self):

        group_request_new = GroupRequest.objects.create_group(recipient=self.recipient,sender=self.sender,group=self.group,status='Pending',is_accepted=False)

        self.assertIsNotNone(group_request_new)
        self.assertEqual(group_request_new.recipient, self.recipient)
        self.assertEqual(group_request_new.sender, self.sender)
        self.assertEqual(group_request_new.group, self.group)
        self.assertEqual(group_request_new.status, 'Pending')
        self.assertFalse(group_request_new.is_accepted)