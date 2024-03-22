from django.test import TestCase
from journal.models import Entry, User
from journal.forms import EditJournalBioForm


class EditJournalBioFormTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.journal = Entry.objects.create(
            journal_title= 'My 21st birthday',
            journal_description= 'x' * 1000,
            journal_bio= 'x' * 10000,
            journal_mood= 'Happy'
        )

    def test_journal_bio_is_not_empty(self):
        self.client.force_login(self.user)

        data = {'new_bio': ''}
        form = EditJournalBioForm(data, instance=self.journal)

        self.assertFalse(form.is_valid())

        self.assertIn('new_bio', form.errors)
        self.assertIn('This field is required.', form.errors['new_bio'])


        unchanged_journal = Entry.objects.get(id=self.journal.id)
        self.assertEqual(unchanged_journal.journal_bio, 'x' * 10000)
    
    def test_edit_journal_bio_is_not_too_long(self):
        self.client.force_login(self.user)

        # Create form data with a bio longer than 10000 characters
        long_bio = 'a' * 10001  
        data = {'new_bio': long_bio}
        form = EditJournalBioForm(data, instance=self.journal)

        # Ensure the form is not valid
        self.assertFalse(form.is_valid())

        # Check that the form contains an error for the title length
        self.assertIn('new_bio', form.errors)
        self.assertIn('Ensure this entry has at most 10000 characters (it has {})'.format(len(long_bio)), form.errors['new_bio'])

        # Ensure the journal title remains unchanged
        unchanged_journal = Entry.objects.get(id=self.journal.id)
        self.assertEqual(unchanged_journal.journal_description, 'x' * 10000)