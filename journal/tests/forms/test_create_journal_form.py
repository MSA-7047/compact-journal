from django.test import TestCase
from journal.forms import CreateJournalForm

class CreateJournalFormTest(TestCase):

    def setUp(self):
        self.form_input = {
            'journal_title': 'My 21st birthday',
            'journal_description': 'x' * 1000,
            'journal_bio': 'x' * 10000,
            'journal_mood': 'Happy',
        }


