from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from journal.models import Journal
from journal.forms import JournalFilterForm, JournalSortForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

class MyJournalsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user1', email='test_user1@example.com', password='test_password')
        self.client.login(username='test_user1', password='test_password')
        self.other_user = get_user_model().objects.create_user(username='test_user2', email='test_user2@example.com', password='test_password')
        self.journal = Journal.objects.create(journal_title='Test Journal', journal_owner=self.user)

    def test_get_request_authenticated(self):
        response = self.client.get(reverse('my_journals', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_journals.html')

    def test_post_request_valid_data(self):
        data = {'filter_field': 'filter_value', 'sort_by_entry_date': 'descending'}
        response = self.client.post(reverse('my_journals', args=[self.user.id]), data)
        self.assertEqual(response.status_code, 200)  # Check if the form is re-rendered
        # Add more assertions based on the expected behavior

    def test_post_request_invalid_data(self):
        data = {'invalid_field': 'invalid_value'}
        response = self.client.post(reverse('my_journals', args=[self.user.id]), data)
        self.assertEqual(response.status_code, 200)  # Check if the form is re-rendered with errors
        # Add more assertions based on the expected behavior

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('my_journals', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected to login page

    # def test_access_other_user_journals(self):
    #     response = self.client.get(reverse('my_journals', args=[self.other_user.id]))
    #     self.assertEqual(response.status_code, 403)  # Check if the user gets forbidden access
