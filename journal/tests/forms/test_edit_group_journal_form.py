from django.test import TestCase
from journal.forms import EditGroupJournalForm
from journal.models import GroupJournal

class EditGroupJournalFormTestCase(TestCase):

    def test_valid_form(self):
        form_data = {
            'journal_title': 'Test Journal Title',
            'journal_description': 'Test Journal Description',
            'journal_bio': 'Test Journal Bio',
            'journal_mood': 'Happy',
            'private': False,
        }
        form = EditGroupJournalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form_data = {}
        form = EditGroupJournalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_title'], ['This field is required.'])
        self.assertEqual(form.errors['journal_description'], ['This field is required.'])
        self.assertEqual(form.errors['journal_mood'], ['This field is required.'])

    def test_long_journal_description(self):
        form_data = {
            'journal_title': 'Test Journal Title',
            'journal_description': 'x' * 1001,  # exceeding the limit by 1
            'journal_bio': 'Test Journal Bio',
            'journal_mood': 'Happy',
            'private': False,
        }
        form = EditGroupJournalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_description'], ['Ensure this value has at most 1000 characters (it has 1001).'])

    def test_long_journal_bio(self):
        form_data = {
            'journal_title': 'Test Journal Title',
            'journal_description': 'Test Journal Description',
            'journal_bio': 'x' * 10001,  # exceeding the limit by 1
            'journal_mood': 'Happy',
            'private': False,
        }
        form = EditGroupJournalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['journal_bio'], ['Ensure this value has at most 10000 characters (it has 10001).'])
