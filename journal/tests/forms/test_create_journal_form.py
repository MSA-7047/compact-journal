from django.test import TestCase
from journal.models import Journal
from journal.forms import CreateJournalForm

class CreateJournalFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'title': 'Test Journal',
            'summary': 'This is a test summary.',
            'private': True
        }
        form = CreateJournalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        form_data = {}
        form = CreateJournalForm(data=form_data)
        self.assertFalse(form.is_valid())


