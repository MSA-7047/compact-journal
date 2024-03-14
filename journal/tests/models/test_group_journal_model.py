from django.test import TestCase
from journal.models import *
from journal.models.GroupJournal import GroupJournal
from django.utils import timezone

class GroupMembershipTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="@test_user", password='Password123', email="test@hotmail.com")
        self.group = Group.objects.create(name="Test Group")
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.journal = GroupJournal.objects.create(
            journal_title='Test Journal',
            journal_description='Description of the test journal.',
            journal_bio='Bio of the test journal.',
            entry_date=timezone.now(),
            journal_mood='Happy',
            journal_group=self.group
        )
    
    def test_journal_name_is_valid(self):
        self.journal.journal_title = 'Test Journal'