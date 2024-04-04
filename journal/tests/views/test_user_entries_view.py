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
        self.user2 = User.objects.get(username='@janedoe')
        self.client.login(username='@johndoe', password='Password123')
        self.journal = Journal.objects.create(title="Test Journal", summary="Test Summary", owner=self.user)
        self.journal2 = Journal.objects.create(title="Test Journal 2", summary="Test Summary 2", owner=self.user2)
        self.entry = Entry.objects.create(title="Test Entry", content="Test Content",summary="test summary", owner=self.user, journal=self.journal, mood="Happy")
        self.entry2 = Entry.objects.create(title="Test Entry2", content="Test Content2",summary="test summary2", owner=self.user2, journal=self.journal2, mood="Happy")
        self.entry_data = {
            'title': 'New Entry',
            'content': 'New Content',
            'summary': 'New Summary',
            'mood': 'Happy'
        }

    def test_view_entry(self):
        response = self.client.get(reverse('view_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_entry.html')

    def test_view_entry_invalid_entry(self):
        response = self.client.post(reverse('view_entry', args=[999])) 
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_create_entry(self):
        self.client.post(reverse('delete_entry', args=[self.entry.id]))
        response = self.client.post(reverse('create_entry', args=[self.journal.id]), self.entry_data)
        self.assertEqual(response.status_code, 302)  
        created_entry = Entry.objects.filter(title='New Entry').exists()
        self.assertTrue(created_entry)
    
    def test_create_entry_invalid_data(self):
        self.client.post(reverse('delete_entry', args=[self.entry.id]))
        self.entry_data = {}
        response = self.client.post(reverse('create_entry', args=[self.journal.id]), self.entry_data)
        self.assertEqual(response.status_code, 200)  
        created_entry = Entry.objects.filter(title='New Entry').exists()
        self.assertFalse(created_entry)

    def test_create_entry_user_not_journal_owner(self):
        self.client.post(reverse('delete_entry', args=[self.entry2.id]))
        response = self.client.post(reverse('create_entry', args=[self.journal2.id]), self.entry_data)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.url, reverse('dashboard'))
        created_entry = Entry.objects.filter(title='New Entry').exists()
        self.assertFalse(created_entry)
    
    def test_create_entry_GET(self):
        self.client.post(reverse('delete_entry', args=[self.entry.id]))
        response = self.client.get(reverse('create_entry',args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_entry.html')
        self.assertEqual(response.context['title'], "Create Entry")

    def test_edit_entry(self):
        response = self.client.post(reverse('edit_entry', args=[self.entry.id]), {'title': 'Updated Entry', 'content': 'Updated Content', 'summary': "update summary", "mood": "Happy"})
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, 'Updated Entry')
    
    def test_edit_entry_GET(self):
        response = self.client.get(reverse('edit_entry',args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_entry.html')
        self.assertEqual(response.context['title'], "Update Entry")

    def test_edit_entry_invalid_data(self):
        response = self.client.post(reverse('edit_entry', args=[self.entry.id]), {})
        self.assertEqual(response.status_code, 200)
        self.entry.refresh_from_db()
        self.assertNotEqual(self.entry.title, 'Updated Entry')
    
    def test_edit_entry_invalid_entry(self):
        response = self.client.post(reverse('edit_entry', args=[999]))  
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_edit_entry_invalid_entry_owner(self):
        response = self.client.post(reverse('edit_entry', args=[self.entry2.id]))  
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_delete_entry(self):
        response = self.client.post(reverse('delete_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Entry.objects.filter(id=self.entry.id).exists())

    def test_delete_entry_invalid_entry(self):
        response = self.client.post(reverse('delete_entry', args=[999]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
    
    def test_delete_entry_invalid_owner(self):
        response = self.client.post(reverse('delete_entry', args=[self.entry2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_view_journal_entries(self):
        response = self.client.post(reverse('journal_entries', args=[self.user2.id, self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_all_journal_entries.html')


    def test_view_journal_entries_get(self):
        response = self.client.get(reverse('journal_entries', args=[self.user.id, self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_all_journal_entries.html')

    def test_existing_entry_for_today(self):
        Entry.objects.create(title="Existing Entry", content="Existing Content", summary="Existing Summary", mood="Sad", owner=self.user, journal=self.journal)
        response = self.client.post(reverse('create_entry', args=[self.journal.id]), {'title': 'Existing Entry', 'content': 'New Content', 'summary': 'New Summary', 'mood': 'Happy'})
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Entry.objects.filter(title='Existing Entry').count(), 1) 

    def test_entry_creation_invalid_journal_id(self):
        invalid_journal_id = 999  
        response = self.client.post(reverse('create_entry', args=[invalid_journal_id]), {'title': 'New Entry', 'content': 'New Content', 'summary': 'New Summary', 'mood': 'Happy'})
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(Entry.objects.filter(title='New Entry').exists())