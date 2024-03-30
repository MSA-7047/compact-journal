from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from journal.models import Journal
from journal.forms import CreateJournalForm
from django.contrib.auth import get_user_model


class EditJournalViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', password='test_password')
        self.journal = Journal.objects.create(journal_title='Test Journal', journal_owner=self.user)

    def test_get_request(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('edit_journal', args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_journal.html')
        self.assertIsInstance(response.context['form'], CreateJournalForm)
        self.assertEqual(response.context['journal'], self.journal)
        self.assertEqual(response.context['title'], "Update Journal")

    def test_post_request_valid_data(self):
        self.client.login(username='test_user', password='test_password')
        data = {
                'journal_title': 'Updated Journal Title',
                'journal_description': 'Updated description',
                'journal_bio': 'Updated bio',
                'journal_mood': 'Sad',
                # Add other fields as needed for form submission
            }
        response = self.client.post(reverse('edit_journal', args=[self.journal.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful edit
        self.journal.refresh_from_db()  # Refresh the journal instance from the database
        self.assertEqual(self.journal.journal_title, 'Updated Journal Title')
        self.assertEqual(self.journal.journal_description, 'Updated description')
        self.assertEqual(self.journal.journal_bio, 'Updated bio')
        self.assertEqual(self.journal.journal_mood, 'Sad')
        # Add assertions for other fields as needed


    def test_post_request_invalid_data(self):
        self.client.login(username='test_user', password='test_password')
        data = {}  # Empty data should result in invalid form
        response = self.client.post(reverse('create_journal'), data)  # Using the correct URL for creating a journal
        self.assertEqual(response.status_code, 200)  # Form should be re-rendered with errors
        self.assertFormError(response, 'form', 'journal_title', 'This field is required.')  # Check for specific form errors
        # Add assertions for other form errors as needed
        self.assertFormError(response, 'form', 'journal_description', 'This field is required.')
        self.assertFormError(response, 'form', 'journal_mood', 'This field is required.')
        # Add assertions for other fields as needed

