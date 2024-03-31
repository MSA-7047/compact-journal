from django.test import TestCase
from django.contrib.auth.models import User
from journal.models import Journal, User, Entry
from django.core.exceptions import ValidationError

class EntryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="@test_user", password='Password123', email="test@hotmail.com")
        self.journal = Journal.objects.create(journal_title = 'Test Entry', journal_summary = 'This is a test Journal summary')
        self.entry = Entry.objects.create(title='Test Entry',
            summary='This is a test Entry summary.',
            content='This is a test Entry content.',
            mood='Happy',
            owner=self.user,
            private=True
            journal = self.journal)

    def test_create_Entry(self):
        # Check if the instance is saved successfully
        self.assertIsNotNone(self.entry.pk)

    def test_entry_fields(self):

        # Retrieve the instance from the database
        retrieved_entry = Entry.objects.get(pk=self.entry.pk)

        # Check if the fields are saved correctly
        self.assertEqual(retrieved_entry.title, 'Test Entry')
        self.assertEqual(retrieved_entry.summary, 'This is a test Entry summary.')
        self.assertEqual(retrieved_entry.content, 'This is a test Entry content.')
        self.assertEqual(retrieved_entry.mood, 'Happy')
        self.assertEqual(retrieved_entry.owner, self.user)
        self.assertEqual(retrieved_entry.jorunal, self.journal)
        self.assertTrue(retrieved_entry.private, True)

    def test_valid_entry_title(self):
        # Create a Entry instance with a valid title
        valid_title_entry = self.entry
        valid_title_entry.full_clean()  # Should not raise any errors

        # Check if the instance is saved successfully
        self.assertIsNotNone(valid_title_entry.pk)
    
    def test_valid_entry_title_at_max_length(self):
        valid_title_entry = self.entry.title = 'A' * 30  # At max length
        valid_title_entry.full_clean()  # This should not raise a error

    def test_invalid_entry_title_max_length(self):
        # Try to create a Entry instance with a title exceeding max length
        with self.assertRaises(ValueError):
            invalid_title_entry = self.entry.title = 'A' * 31  # Exceeds max length
            invalid_title_entry.full_clean()  # This should raise a ValueError

    def test_invalid_entry_title_empty(self):
        # Try to create a Entry instance with an empty title
        with self.assertRaises(ValueError):
            empty_title_entry = self.entry.title = ''
            empty_title_entry.full_clean()  # This should raise a ValueError
            
    def test_valid_entry_summary(self):
        # Create a Entry instance with a valid summary
        valid_summary_entry = self.entry
        valid_summary_entry.full_clean()  # Should not raise any errors

        # Check if the instance is saved successfully
        self.assertIsNotNone(valid_summary_entry.pk)
    
     def test_valid_entry_summary_at_max_length(self):
        valid_summary_entry = self.entry.title = 'A' * 150  # Exceeds max length
        valid_summary_entry.full_clean()  # This should raise a ValueError


    def test_invalid_entry_summary_above_max_length(self):
        # Try to create a Entry instance with a summary exceeding max length
        with self.assertRaises(ValueError):
            invalid_summary_entry = self.entry.summary = 'A' * 151 
            invalid_summary_entry.full_clean()  # This should raise a ValueError

    # def test_invalid_entry_summary_empty(self):
    #     # Try to create a Entry instance with an empty summary
    #     with self.assertRaises(ValueError):
    #         empty_summary_Entry = s
    #         empty_summary_Entry.full_clean()  # This should raise a ValueError

    def test_valid_entry_content(self):
        # Create a Entry instance with a valid content
        valid_content_entry = self.entry
        valid_content_entry.full_clean()  # Should not raise any errors

        # Check if the instance is saved successfully
        self.assertIsNotNone(valid_content_entry.pk)
    
    def test_valid_entry_content_at_max_length(self):
        valid_content_entry = self.entry.title = 'A' * 10000  # At max length
        valid_content_entry.full_clean()  # This should not raise an error

    def test_invalid_entry_content_max_length(self):
        # Try to create a Entry instance with a content exceeding max length
        with self.assertRaises(ValueError):
            invalid_content_entry = self.entry.content = 'A' * 10001
            invalid_content_entry.full_clean()  # This should raise a ValueError

    # def test_invalid_entry_content_empty(self):
    #     # Try to create a Entry instance with an empty content
    #     with self.assertRaises(ValueError):
    #         empty_content_Entry = 
    #         empty_content_Entry.full_clean()  # This should raise a ValueError
    
    def test_mood_can_be_happy(self):
        happy_entry = self.entry.mood = 'Happy'
        self.assertEqual(self.entry.mood, 'Happy')

    def test_mood_can_be_sad(self):
       Sad_entry = self.entry.mood = 'Sad'
       self.assertEqual(self.entry.mood, 'Sad')

    def test_mood_can_be_angry(self):
        angry_entry = self.entry.mood = 'Angry'
        self.assertEqual(self.entry.mood, 'Angry')
       

    def test_mood_can_be_neutral(self):
        neutral_entry = self.entry.mood = 'Neutral'
        self.assertEqual(self.entry.mood, 'Neutral')
    

    def test_mood_cant_be_empty(self):
         # Try to create a Entry instance with a empty mood
        with self.assertRaises(ValueError):
            empty_mood_entry = self.entry.mood = ''
            empty_mood_entry.full_clean()  # This should raise a ValueError
