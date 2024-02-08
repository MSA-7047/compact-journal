from django.test import TestCase
from journal.forms import CreateJournalForm
from journal.models import Journal

class CreateJournalFormTest(TestCase):

    def setUp(self):
        self.form_input = {

            'journal_title': 'My 21st birthday',
            'journal_description': 'x' * 1000,
            'journal_bio': 'x' * 10000,
            'journal_mood': 'Happy',
        }
    
    def test_valid_journal_form(self):
        form = CreateJournalForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_journal_description(self):
        self.form_input['journal_description'] = ''
        form = CreateJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_description'], ['This field is required.', 'Journal Description cannot be blank'])
    
    def test_blank_journal_bio(self):
        self.form_input['journal_bio'] = ''
        form = CreateJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_bio'], ['This field is required.', 'Journal Entry cannot be blank'])

    def test_blank_journal_mood(self):
        self.form_input['journal_mood'] = ''
        form = CreateJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_Mood'], ['This field is required.', 'Journal Mood cannot be blank'])

    def test_long_journal_description(self):
        self.form_input['journal_description'] = 'x' * 1000
        form = CreateJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_description'], ['Journal Description length cannot exceed 1000 characters'])

    def test_long_journal_bio(self):
        self.form_input['journal_bio'] = 'x' * 10000
        form = CreateJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_bio'], ['Journal Entry length cannot exceed 10000 characters'])

