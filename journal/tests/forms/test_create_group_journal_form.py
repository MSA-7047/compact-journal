from django.test import TestCase
from journal.forms import CreateGroupJournalForm

class CreateGroupJournalFormTest(TestCase):

    def setUp(self):
        self.form_input = {
            'title': 'My 21st birthday',
            'summary': 'x' * 200,
            'content': 'x' * 10000,
            'mood': 'Happy',
        }
    
    def test_valid_journal_form(self):
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_summary_is_invalid(self):
        self.form_input['summary'] = ''
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['summary'], ['This field is required.'])

    def test_blank_content_is_valid(self):
        self.form_input['content'] = ''
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_mood_is_invalid(self):
        self.form_input['mood'] = ''
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['mood'], ['This field is required.'])

    def test_long_summary(self):
        self.form_input['summary'] = 'x' * 1001  # Exceeding the limit by 1
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['summary'], ['Ensure this value has at most 200 characters (it has 1001).'])

    def test_long_content(self):
        self.form_input['content'] = 'x' * 10001  # Exceeding the limit by 1
        form = CreateGroupJournalForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'], ['Ensure this value has at most 10000 characters (it has 10001).'])
