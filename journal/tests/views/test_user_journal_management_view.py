from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Journal, User

class JournalViewsTest(TestCase):

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
        self.journal2 = Journal.objects.create(title="Test Journal", summary="Test Summary", owner=self.user2)

    
    def test_create_journal_view(self):
        response = self.client.post(reverse('create_journal'), {'title': 'New Journal', 'summary': 'New Summary'})
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received

        # Check if the journal is created in the database
        created_journal = Journal.objects.filter(title='New Journal').exists()
        self.assertTrue(created_journal)

    def test_edit_journal_view(self):
        response = self.client.post(reverse('edit_journal', args=[self.journal.id]), {'title': 'Edited Journal', 'summary': 'Edited Summary'})
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received

        # Check if the journal is edited in the database
        edited_journal = Journal.objects.get(id=self.journal.id)
        self.assertEqual(edited_journal.title, 'Edited Journal')
        self.assertEqual(edited_journal.summary, 'Edited Summary')

    def test_edit_journal_user_not_owner(self):
        response = self.client.post(reverse('edit_journal', args=[self.journal2.id]), {'title': 'Edited Journal', 'summary': 'Edited Summary'})
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received

        # Check if the journal is not edited in the database
        edited_journal = Journal.objects.get(id=self.journal2.id)
        self.assertNotEqual(edited_journal.title, 'Edited Journal')
        self.assertNotEqual(edited_journal.summary, 'Edited Summary')

    def test_delete_journal_view(self):
        response = self.client.post(reverse('delete_journal', args=[self.journal.id]))
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received
        deleted_journal = Journal.objects.filter(id=self.journal.id).exists()
        self.assertFalse(deleted_journal)

    def test_delete_journal_user_not_owner(self):
        response = self.client.post(reverse('delete_journal', args=[self.journal2.id]), {'title': 'Edited Journal', 'summary': 'Edited Summary'})
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received

        # Check if the journal is not edited in the database
        deleted_journal = Journal.objects.filter(id=self.journal2.id).exists()
        self.assertTrue(deleted_journal)

    def test_all_journals_view(self):
        response = self.client.get(reverse('view_journals', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)  # Check if success status code is received

    def test_all_journals_view_invalid_user(self):
        response = self.client.get(reverse('view_journals', args=[999]))
        self.assertEqual(response.status_code, 302)  # Check if success status code is received

    def test_journal_dashboard_view(self):
        response = self.client.get(reverse('journal_dashboard', args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)  # Check if success status code is received
        self.assertTemplateUsed(response, 'journal_dashboard.html')
        self.assertEqual(response.context['journal'], self.journal)

    def test_edit_journal_view_permissions(self):
        self.client.logout()
        self.client.login(username='@janedoe', password='Password123')
        response = self.client.post(reverse('edit_journal', args=[self.journal.id]), {'title': 'Edited Journal', 'summary': 'Edited Summary'})
        self.assertEqual(response.status_code, 302)
        self.journal.refresh_from_db()
        self.assertNotEqual(self.journal.title, 'Edited Journal')
        self.assertNotEqual(self.journal.summary, 'Edited Summary')

    def test_delete_journal_view_permissions(self):
        self.client.logout()
        self.client.login(username='@janedoe', password='Password123')
        response = self.client.post(reverse('delete_journal', args=[self.journal.id]))
        self.assertEqual(response.status_code, 302)
        journal_exists = Journal.objects.filter(id=self.journal.id).exists()
        self.assertTrue(journal_exists)

    def test_edit_journal_view_error_handling(self):
        response = self.client.post(reverse('edit_journal', args=[999]))  # Non-existent journal ID
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_delete_journal_view_error_handling(self):
        response = self.client.post(reverse('delete_journal', args=[999]))  # Non-existent journal ID
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))