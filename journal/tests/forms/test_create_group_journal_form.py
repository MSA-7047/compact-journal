from django.test import TestCase
from journal.forms import CreateGroupJournalForm

class CreateGroupJournalFormTest(TestCase):

    def setUp(self):
        self.form_input = {
            'journal_title': 'My 21st birthday',
            'journal_description': 'x' * 1000,
            'journal_bio': 'x' * 10000,
            'journal_mood': 'Happy',
        }
    
    def test_valid_journal_form(self):
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_journal_description_is_invalid(self):
        self.form_input['journal_description'] = ''
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_description'], ['This field is required.'])

    def test_blank_journal_bio_is_valid(self):
        self.form_input['journal_bio'] = ''
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_journal_mood_is_invalid(self):
        self.form_input['journal_mood'] = ''
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_mood'], ['This field is required.'])

    def test_long_journal_description(self):
        self.form_input['journal_description'] = 'x' * 1001  # exceeding the limit by 1
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_description'], ['Ensure this value has at most 1000 characters (it has 1001).'])

    def test_long_journal_bio(self):
        self.form_input['journal_bio'] = 'x' * 10001  # exceeding the limit by 1
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_bio'], ['Ensure this value has at most 10000 characters (it has 10001).'])
