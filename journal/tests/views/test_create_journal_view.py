# from django.test import TestCase
# from django.urls import reverse
# from journal.models import Journal
# from journal.forms import CreateJournalForm

# class CreateJournalViewTestCase(TestCase):

#     def setUp(self):
#         self.url = reverse('create_journal_view')
#         self.form_input = {

#             'journal_title': 'My 21st birthday',
#             'journal_description': 'x' * 1000,
#             'journal_bio': 'x' * 10000,
#             'journal_mood': 'Happy',
#         }

#     def test_create_journal_view_url(self):
#         self.assertEqual(self.url,'/create_journal_view/')

    
#     def test_unsuccesful_journal_creation(self):
#         self.form_input['journal_description'] = 'x' * 1001
#         before_count = Journal.objects.count()
#         response = self.client.post(self.url, self.form_input)
#         after_count = Journal.objects.count()
#         self.assertEqual(after_count, before_count)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'create_journal_view.html')
#         form = response.context['form']
#         self.assertTrue(isinstance(form, CreateJournalForm))
#         self.assertTrue(form.is_bound)
#         self.assertFalse(self._is_logged_in())
    
#     def test_succesful_journal_creation(self):
#         before_count = Journal.objects.count()
#         response = self.client.post(self.url, self.form_input, follow=True)
#         after_count = Journal.objects.count()
#         self.assertEqual(after_count, before_count+1)
#         response_url = reverse('dashboard')
#         self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
#         self.assertTemplateUsed(response, 'dashboard.html')
#         journal = Journal.objects.get(journal_title='My 21st birthday')
#         self.assertEqual(journal.description, 'x' * 1000)
#         self.assertEqual(journal.bio, 'x' * 10000)
#         self.assertEqual(journal.mood, 'Happy')
#         self.assertTrue(self._is_logged_in())

from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Entry
from django.contrib.auth.models import User
from datetime import datetime
from journal.models import Journal
from journal.forms import CreateJournalForm
from django.contrib.auth import get_user_model


class CreateJournalViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', password='test_password')

    # def test_get_request(self):
    #     response = self.client.get(reverse('create_journal'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'create_journal.html')

    def test_post_request_valid_data(self):
        data = {
            'journal_title': 'Test Journal',
            'journal_description': 'Test description',
            'journal_bio': 'Test bio',
            'journal_mood': 'Happy',
        }
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(reverse('create_journal'), data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation
        self.assertEqual(Journal.objects.count(), 1)  # One journal should be created
        journal = Journal.objects.first()
        self.assertEqual(journal.journal_title, 'Test Journal')
        self.assertEqual(journal.journal_description, 'Test description')
        self.assertEqual(journal.journal_bio, 'Test bio')
        self.assertEqual(journal.journal_mood, 'Happy')
        self.assertEqual(journal.journal_owner, self.user)

    def test_post_request_invalid_data(self):
        data = {}  # Empty data should result in invalid form
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(reverse('create_journal'), data)
        self.assertEqual(response.status_code, 200)  # Form should be re-rendered with errors
        self.assertFormError(response, 'form', 'journal_title', 'This field is required.')  # Check for specific form errors
        self.assertEqual(Journal.objects.count(), 0)  # No journals should be created


    
