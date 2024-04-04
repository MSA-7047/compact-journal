from django.test import TestCase
from django.contrib.auth.models import User
from journal.models import Journal, User, Entry
from django.utils import timezone
from django.core.exceptions import ValidationError

class EntryTestCase(TestCase):
     """Unit tests for the Entry model."""
     
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

        # Assert that the retrieved entry matches the created entry.
        self.assertEqual(retrieved_entry.title, 'Test Entry')
        self.assertEqual(retrieved_entry.summary, 'This is a test Entry summary.')
        self.assertEqual(retrieved_entry.content, 'This is a test Entry content.')
        self.assertEqual(retrieved_entry.mood, 'Happy')
        self.assertEqual(retrieved_entry.owner, self.user)
        self.assertEqual(retrieved_entry.private, True)
        self.assertEqual(retrieved_entry.journal, self.journal)

        retrieved_entry.full_clean()

    def test_entry_fields(self):

        self.assertEqual(self.entry._meta.get_field('title').verbose_name, 'Title')
        self.assertEqual(self.entry._meta.get_field('summary').max_length, 200)
        self.assertEqual(self.entry._meta.get_field('content').max_length, 10000)
        
    def test_valid_entry_title_at_max_length(self):
        self.entry.title = 'A' * 30  
        self.entry.full_clean()  # This should not raise a error

    def test_invalid_entry_title_above_max_length(self):
        with self.assertRaises(ValidationError):
            self.entry.title = 'A' * 31  
            self.entry.full_clean()  # This should raise a ValueError

    def test_invalid_entry_title_empty(self):
        with self.assertRaises(ValidationError):
            self.entry.title = ''
            self.entry.full_clean()  # This should raise a ValueError
            
    def test_valid_entry_summary_at_max_length(self):
        self.entry.summary = 'A' * 200 
        self.entry.full_clean()  # This should raise a ValueError

    def test_valid_entry_content_at_max_length(self):
        self.entry.content = 'A' * 10000  
        self.entry.full_clean()  # This should not raise an error
    
    def test_mood_cant_be_empty(self): 
        with self.assertRaises(ValidationError):
            self.entry.mood = ''
            self.entry.full_clean()  # This should raise a ValueError

