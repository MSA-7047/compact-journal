from django.test import TestCase
from journal.forms import CreateEntryForm

class CreateEntryFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            'title': 'Test Entry',
            'summary': 'This is a test summary.',
            'content': 'This is a test content.',
            'mood': 'Happy',
            'private': True
        }

    def test_valid_form(self):
        form = CreateEntryForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        self.form_data["title"] = ''
        form = CreateEntryForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_content_not_required(self):
        self.form_data["content"] = ''
        form = CreateEntryForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_mood(self):
        self.form_data["mood"] = 'unknown'
        form = CreateEntryForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mood', form.errors)
