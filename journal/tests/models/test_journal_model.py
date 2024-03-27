from django.test import TestCase
from django.contrib.auth.models import User
from journal.models import User, Journal
from django.core.exceptions import ValidationError
from journal.forms import CreateJournalForm


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
        with self.assertRaises(ValidationError) as context:
            invalid_title_journal = Journal(
                journal_title='A' * 51 , # Exceeds max length
                journal_description='This is a valid description.',
                journal_bio='This is a valid bio.',
                journal_mood='Happy',
                journal_owner=self.user,
                private=True
            )
            invalid_title_journal.full_clean()

        # Check if the ValidationError contains the correct error message
        self.assertIn('Ensure this value has at most 50 characters', str(context.exception))



    def test_invalid_journal_title_empty(self):
        # Try to create a Journal instance with an empty title
        form_input = {
            'journal_title': '',
            'journal_description': 'B' * 1000,
            'journal_bio': 'C' * 10000,
            'journal_mood': 'Happy',
            'journal_owner': self.user,
            'private': True
        }
        
        # Instantiate the form with the provided data
        form = CreateJournalForm(data=form_input)
        
        # Assert that the form is not valid
        self.assertFalse(form.is_valid())
        
        # Assert that the correct error message is present in non-field errors
        self.assertEqual(form.errors['journal_title'], ['This field is required.'])
            
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

        # Save the instance to the database
        valid_description_journal.save()

        # Check if the instance is saved successfully
        self.assertIsNotNone(valid_description_journal.pk)


    def test_journal_description_max_length(self):
        # Prepare form input with a description exceeding the maximum length
        form_input = {
            'journal_title': 'A' * 50,
            'journal_description': 'D' * 1001,  # Exceeds max length
            'journal_bio': 'This is a valid bio.',  
            'journal_mood': 'Happy',
            'journal_owner': self.user,
            'private': True
        }
        
        # Instantiate the form with the provided data
        form = CreateJournalForm(data=form_input)
        
        # Assert that the form is not valid
        self.assertFalse(form.is_valid())
        
        # Assert that the correct error message is present in non-field errors
        self.assertEqual(form.errors['journal_description'], ['Ensure this value has at most 1000 characters (it has 1001).'])
            

    def test_invalid_journal_description_empty(self):
        # Try to create a Journal instance with an empty description

        form_input = {
            'journal_title': 'Test Title',
            'journal_description': '' ,
            'journal_bio': 'C' * 10000,
            'journal_mood': 'Happy',
            'journal_owner': self.user,
            'private': True
        }
        
        # Instantiate the form with the provided data
        form = CreateJournalForm(data=form_input)
        
        # Assert that the form is not valid
        self.assertFalse(form.is_valid())
        
        # Assert that the correct error message is present in non-field errors
        self.assertEqual(form.errors['journal_description'], ['This field is required.'])


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
        
        valid_bio_journal.save()

        # Check if the instance is saved successfully
        self.assertIsNotNone(valid_bio_journal.pk)

    def test_journal_bio_max_length(self):
        # Prepare form input with a description exceeding the maximum length
        form_input = {
            'journal_title': 'A' * 50,
            'journal_description': 'B' * 1000,
            'journal_bio': 'C' * 10001,  # Exceeds max length
            'journal_mood': 'Happy',
            'journal_owner': self.user,
            'private': True
        }
        
        # Instantiate the form with the provided data
        form = CreateJournalForm(data=form_input)
        
        # Assert that the form is not valid
        self.assertFalse(form.is_valid())
        
        # Assert that the correct error message is present in non-field errors
        self.assertEqual(form.errors['journal_bio'], ['Ensure this value has at most 10000 characters (it has 10001).'])

