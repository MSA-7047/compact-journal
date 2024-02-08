from django.test import TestCase
from journal.models import Journal, User
from journal.forms import EditJournalDescriptionForm


class EditJournalDescriptionFormTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.journal = Journal.objects.create(
            journal_title= 'My 21st birthday',
            journal_description= 'x' * 1000,
            journal_bio= 'x' * 10000,
            journal_mood= 'Happy'
        )

    def test_journal_description_is_not_empty(self):
        self.client.force_login(self.user)

        data = {'new_description': ''}
        form = EditJournalDescriptionForm(data, instance=self.journal)

        self.assertFalse(form.is_valid())

        self.assertIn('new_description', form.errors)
        self.assertIn('This field is required.', form.errors['new_description'])


        unchanged_journal = Journal.objects.get(id=self.journal.id)
        self.assertEqual(unchanged_journal.journal_description, 'x' * 1000)
    
    def test_edit_journal_description_is_not_too_long(self):
        self.client.force_login(self.user)

        # Create form data with a description longer than 1000 characters
        long_description = 'a' * 1001  
        data = {'new_description': long_description}
        form = EditJournalDescriptionForm(data, instance=self.journal)

        # Ensure the form is not valid
        self.assertFalse(form.is_valid())

        # Check that the form contains an error for the title length
        self.assertIn('new_description', form.errors)
        self.assertIn('Ensure this value has at most 1000 characters (it has {})'.format(len(long_description)), form.errors['new_description'])

        # Ensure the journal title remains unchanged
        unchanged_journal = Journal.objects.get(id=self.journal.id)
        self.assertEqual(unchanged_journal.journal_description, 'x' * 1000)