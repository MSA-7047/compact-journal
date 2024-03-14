from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from journal.models import Journal
from django.contrib.auth import get_user_model


class JournalDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.journal = Journal.objects.create(journal_title='Test Journal', journal_owner=self.user)

    def test_journal_detail_view(self):
        response = self.client.get(reverse('journal_detail', args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)  # Check if the page loads successfully
        self.assertTemplateUsed(response, 'journal_detail.html')  # Check if the correct template is used
        self.assertEqual(response.context['user'], self.user)  # Check if the user is passed to the template context
        self.assertEqual(response.context['journal'], self.journal)  # Check if the journal is passed to the template context
