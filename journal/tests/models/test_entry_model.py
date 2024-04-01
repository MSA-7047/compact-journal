from django.test import TestCase
from django.contrib.auth.models import User
from journal.models import Journal, User, Entry
from django.utils import timezone

class EntryTestCase(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.journal = Journal.objects.create(title = 'Test Entry', summary = 'This is a test Journal summary', owner = self.user, private = False)
        self.entry = Entry.objects.create(
            title='Test Entry',
            summary='This is a test Entry summary.',
            content='This is a test Entry content.',
            mood='Happy',
            owner=self.user,
            private=True,
            journal = self.journal)

    def test_entry_creation(self):

        retrieved_entry = Entry.objects.get(pk=self.entry.pk)

        # Assert that the retrieved entry matches the created entry
        self.assertEqual(retrieved_entry.title, 'Test Entry')
        self.assertEqual(retrieved_entry.summary, 'This is a test Entry summary.')
        self.assertEqual(retrieved_entry.content, 'This is a test Entry content.')
        self.assertEqual(retrieved_entry.mood, 'Happy')
        self.assertEqual(retrieved_entry.owner, self.user)
        self.assertEqual(retrieved_entry.private, True)
        self.assertEqual(retrieved_entry.journal, self.journal)

    def test_entry_fields(self):

        # Assert that the fields have the expected attributes
        self.assertEqual(self.entry._meta.get_field('title').verbose_name, 'Title')
        self.assertEqual(self.entry._meta.get_field('summary').max_length, 200)
        # Add assertions for other fields as needed

