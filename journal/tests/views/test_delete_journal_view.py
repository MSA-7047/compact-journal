from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from journal.models import Journal
from django.contrib.auth import get_user_model


class DeleteJournalViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.journal = Journal.objects.create(journal_title='Test Journal', journal_owner=self.user)

    def test_delete_journal(self):
        response = self.client.post(reverse('my_journals', args=[self.journal.id]))
        self.assertEqual(response.status_code, 302)  # Expecting redirect after successful deletion
        self.assertFalse(Journal.objects.filter(id=self.journal.id).exists())  # Journal should be deleted
        self.assertRedirects(response, reverse('dashboard'))  # Ensure redirection to the dashboard page

