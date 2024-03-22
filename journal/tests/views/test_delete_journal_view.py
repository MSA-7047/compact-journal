from django.test import TestCase
from django.urls import reverse
from journal.models import Entry
from journal.forms import CreateJournalForm

class DeleteJournalViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('delete_journal_view')
        self.form_input = {

            'journal_title': 'My 21st birthday',
            'journal_description': 'x' * 1000,
            'journal_bio': 'x' * 10000,
            'journal_mood': 'Happy',
        }

    def test_delete_journal_view_url(self):
        self.assertEqual(self.url,'/delete_journal_view/')
        

    
    def test_succesful_journal_deletion(self):
        #add journal fscni nsdccbb ibjjmn adib 
        before_count = Entry.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Entry.objects.count()
        self.assertEqual(after_count, before_count - 1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        journal = Entry.objects.get(journal_title='My 21st birthday')
        self.assertTrue(self._is_logged_in())