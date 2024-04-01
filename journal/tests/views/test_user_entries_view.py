from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Journal, Entry, User
from datetime import datetime

class EntryViewTest(TestCase):

    fixtures = [
        'journal/tests/fixtures/default_user.json',
        'journal/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username='@johndoe', password='Password123')
        self.journal = Journal.objects.create(title="Test Journal", summary="Test Summary", owner=self.user)
        self.entry = Entry.objects.create(title="Test Entry", content="Test Content",summary="test summary", owner=self.user, journal=self.journal, mood="Happy")

    def test_view_entry(self):
        response = self.client.get(reverse('view_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_entry.html')

    def test_create_entry(self):
        entry_data = {
            'title': 'New Entry',
            'content': 'New Content',
            'summary': 'New Summary',
            'mood': 'Happy'
        }
        self.client.post(reverse('delete_entry', args=[self.entry.id]))
        response = self.client.post(reverse('create_entry', args=[self.journal.id]), entry_data)
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received

        # Check if the entry is created in the database
        created_entry = Entry.objects.filter(title='New Entry').exists()
        self.assertTrue(created_entry)

    def test_edit_entry(self):
        response = self.client.post(reverse('edit_entry', args=[self.entry.id]), {'title': 'Updated Entry', 'content': 'Updated Content', 'summary': "update summary", "mood": "Happy"})
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, 'Updated Entry')

    def test_delete_entry(self):
        response = self.client.post(reverse('delete_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Entry.objects.filter(id=self.entry.id).exists())

    def test_view_journal_entries(self):
        response = self.client.get(reverse('journal_entries', args=[self.user.id, self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_all_journal_entries.html')

    def test_permission_denied_create_entry(self):
        self.client.logout()
        self.client.login(username='@janedoe', password='Password123')
        response = self.client.post(reverse('create_entry', args=[self.journal.id]), {'title': 'New Entry', 'content': 'New Content', 'summary': 'New Summary', 'mood': 'Happy'})
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received
        self.assertFalse(Entry.objects.filter(title='New Entry').exists())  # Check if entry is not created

    def test_permission_denied_edit_entry(self):
        self.client.logout()
        self.client.login(username='@janedoe', password='Password123')
        response = self.client.post(reverse('edit_entry', args=[self.entry.id]), {'title': 'Updated Entry', 'content': 'New Content', 'summary': 'New Summary', 'mood': 'Happy'})
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received
        self.assertFalse(Entry.objects.filter(title='Updated Entry').exists())  # Check if entry is not created

    def test_delete_entry_wrong_permissions(self):
        self.client.logout()
        self.client.login(username='@janedoe', password='Password123')
        response = self.client.post(reverse('delete_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 302)
        entry_exists = Entry.objects.filter(id=self.entry.id).exists()
        self.assertTrue(entry_exists)

    def test_existing_entry_for_today(self):
        entry = Entry.objects.create(title="Existing Entry", content="Existing Content", summary="Existing Summary", mood="Sad", owner=self.user, journal=self.journal)
        response = self.client.post(reverse('create_entry', args=[self.journal.id]), {'title': 'Existing Entry', 'content': 'New Content', 'summary': 'New Summary', 'mood': 'Happy'})
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received
        self.assertEqual(Entry.objects.filter(title='Existing Entry').count(), 1)  # Check if no additional entry is created

    def test_entry_creation_invalid_journal_id(self):
        invalid_journal_id = 999  # Assuming there's no journal with this ID
        response = self.client.post(reverse('create_entry', args=[invalid_journal_id]), {'title': 'New Entry', 'content': 'New Content', 'summary': 'New Summary', 'mood': 'Happy'})
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received
        self.assertFalse(Entry.objects.filter(title='New Entry').exists())