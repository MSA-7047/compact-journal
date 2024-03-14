from django.test import TestCase
from django.contrib.auth.models import User
from journal.models import User, Journal

class JournalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="@test_user", password='Password123', email="test@hotmail.com")
        self.journal = Journal.objects.create(journal_title='Test Journal',
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
        retrieved_journal = Journal.objects.get(pk=self.journal.pk)

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
        valid_description_journal = Journal(
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

    def test_invalid_journal_description_max_length(self):
        # Try to create a Journal instance with a description exceeding max length
        with self.assertRaises(ValueError):
            invalid_description_journal = Journal(
                journal_title='Invalid Description Journal',
                journal_description='D' * 1001,  # Exceeds max length
                journal_bio='This is a valid bio.',
                journal_mood='Happy',
                journal_owner=self.user,
                private=True
            )
            invalid_description_journal.full_clean()  # This should raise a ValueError

    def test_invalid_journal_description_empty(self):
        # Try to create a Journal instance with an empty description
        with self.assertRaises(ValueError):
            empty_description_journal = Journal(
                journal_title='Empty Description Journal',
                journal_description='',
                journal_bio='This is a valid bio.',
                journal_mood='Happy',
                journal_owner=self.user,
                private=True
            )
            empty_description_journal.full_clean()  # This should raise a ValueError
    def test_valid_journal_bio(self):
        # Create a Journal instance with a valid bio
        valid_bio_journal = Journal(
            journal_title='Valid Bio Journal',
            journal_description='This is a valid description.',
            journal_bio='This is a valid bio.',
            journal_mood='Happy',
            journal_owner=self.user,
            private=True
        )
        valid_bio_journal.full_clean()  # Should not raise any errors

        # Check if the instance is saved successfully
        self.assertIsNotNone(valid_bio_journal.pk)

    def test_invalid_journal_bio_max_length(self):
        # Try to create a Journal instance with a bio exceeding max length
        with self.assertRaises(ValueError):
            invalid_bio_journal = Journal(
                journal_title='Invalid Bio Journal',
                journal_description='This is a valid description.',
                journal_bio='B' * 10001,  # Exceeds max length
                journal_mood='Happy',
                journal_owner=self.user,
                private=True
            )
            invalid_bio_journal.full_clean()  # This should raise a ValueError

    def test_invalid_journal_bio_empty(self):
        # Try to create a Journal instance with an empty bio
        with self.assertRaises(ValueError):
            empty_bio_journal = Journal(
                journal_title='Empty Bio Journal',
                journal_description='This is a valid description.',
                journal_bio='',
                journal_mood='Happy',
                journal_owner=self.user,
                private=True
            )
            empty_bio_journal.full_clean()  # This should raise a ValueError