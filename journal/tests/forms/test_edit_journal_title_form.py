from django.test import TestCase
from journal.models import Entry, User
from journal.forms import EditJournalTitleForm


class EditJournalTitleFormTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.journal = Entry.objects.create(
            journal_title= 'My 21st birthday',
            journal_description= 'x' * 1000,
            journal_bio= 'x' * 10000,
            journal_mood= 'Happy'
        )

    def test_journal_title_is_not_empty(self):
        self.client.force_login(self.user)

        data = {'new_title': ''}
        form = EditJournalTitleForm(data, instance=self.journal)

        self.assertFalse(form.is_valid())

        self.assertIn('new_title', form.errors)
        self.assertIn('This field is required.', form.errors['new_title'])


        unchanged_journal = Entry.objects.get(id=self.journal.id)
        self.assertEqual(unchanged_journal.journal_title, 'My 21st birthday')
    
    def test_edit_journal_title_is_not_too_long(self):
        self.client.force_login(self.user)

        # Create form data with a title longer than 50 characters
        long_title = 'a' * 51  
        data = {'new_title': long_title}
        form = EditJournalTitleForm(data, instance=self.journal)

        # Ensure the form is not valid
        self.assertFalse(form.is_valid())

        # Check that the form contains an error for the title length
        self.assertIn('new_title', form.errors)
        self.assertIn('Ensure this value has at most 50 characters (it has {})'.format(len(long_title)), form.errors['new_title'])

        # Ensure the journal title remains unchanged
        unchanged_journal = Entry.objects.get(id=self.journal.id)
        self.assertEqual(unchanged_journal.journal_title, 'My 21st birthday')


    
