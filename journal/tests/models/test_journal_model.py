from django.test import TestCase
from django.contrib.auth.models import User
from journal.models import Entry, User

class JournalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="@test_user", password='Password123', email="test@hotmail.com")
        self.journal = Entry.objects.create(journal_title='Test Journal',
            journal_description='This is a test journal description.',
            journal_bio='This is a test journal bio.',
            journal_mood='Happy',
            journal_owner=self.user,
            private=True)

    def test_create_journal(self):
        # Check if the instance is saved successfully
        self.assertIsNotNone(self.journal.pk)

    def test_journal_fields(self):

        # Retrieve the instance from the database
        retrieved_journal = Entry.objects.get(pk=self.journal.pk)

        # Check if the fields are saved correctly
        self.assertEqual(retrieved_journal.journal_title, 'Test Journal')
        self.assertEqual(retrieved_journal.journal_description, 'This is a test journal description.')
        self.assertEqual(retrieved_journal.journal_bio, 'This is a test journal bio.')
        self.assertEqual(retrieved_journal.journal_mood, 'Happy')
        self.assertEqual(retrieved_journal.journal_owner, self.user)
        self.assertTrue(retrieved_journal.private)

    def test_valid_journal_title(self):
        # Create a Journal instance with a valid title
        valid_title_journal = self.journal
        valid_title_journal.full_clean()  # Should not raise any errors

        # Check if the instance is saved successfully
        self.assertIsNotNone(valid_title_journal.pk)

    def test_invalid_journal_title_max_length(self):
        # Try to create a Journal instance with a title exceeding max length
        with self.assertRaises(ValueError):
            invalid_title_journal = self.journal.journal_title = 'A' * 51  # Exceeds max length
            invalid_title_journal.full_clean()  # This should raise a ValueError

    def test_invalid_journal_title_empty(self):
        # Try to create a Journal instance with an empty title
        with self.assertRaises(ValueError):
            empty_title_journal = self.journal.journal_title = ''
            empty_title_journal.full_clean()  # This should raise a ValueError
            
    def test_valid_journal_description(self):
        # Create a Journal instance with a valid description
        valid_description_journal = Entry(
            journal_title='Valid Description Journal',
            journal_description='This is a valid description.',
            journal_bio='This is a valid bio.',
            journal_mood='Happy',
            journal_owner=self.user,
            private=True
        )
        valid_description_journal.full_clean()  # Should not raise any errors

        # Check if the instance is saved successfully
        self.assertIsNotNone(valid_description_journal.pk)

    def test_summary_max_length(self):
        max_length = self.journal._meta.get_field('summary').max_length
        self.assertEqual(max_length, 350)

    def test_owner_relation(self):
        owner = self.journal.owner
        self.assertEqual(owner.username, '@johndoe')

    def test_private_default_value(self):
        self.assertFalse(self.journal.private)
