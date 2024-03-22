from django.test import TestCase
from django.urls import reverse
from journal.models import Entry
from journal.forms import CreateJournalForm

class CreateJournalViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('create_journal_view')
        self.form_input = {

            'journal_title': 'My 21st birthday',
            'journal_description': 'x' * 1000,
            'journal_bio': 'x' * 10000,
            'journal_mood': 'Happy',
        }

    def test_create_journal_view_url(self):
        self.assertEqual(self.url,'/create_journal_view/')

    
    def test_unsuccesful_journal_creation(self):
        self.form_input['journal_description'] = 'x' * 1001
        before_count = Entry.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Entry.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_journal_view.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateJournalForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())
    
    def test_succesful_journal_creation(self):
        before_count = Entry.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Entry.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        journal = Entry.objects.get(journal_title='My 21st birthday')
        self.assertEqual(journal.description, 'x' * 1000)
        self.assertEqual(journal.bio, 'x' * 10000)
        self.assertEqual(journal.mood, 'Happy')
        self.assertTrue(self._is_logged_in())

    
