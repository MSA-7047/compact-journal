from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Journal, User





class ChangeJournalDescriptionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.journal = Journal.objects.create(

            journal_title = 'My 21st birthday',
            journal_description= 'x' * 1000,
            journal_bio= 'x' * 10000,
            journal_mood= 'Happy'
        )

    def test_change_journal_description_view_get(self):
        # Test the GET request to the change_journal_description view
        self.client.force_login(self.user)
        response = self.client.get('/change-journal-description/{}/'.format(self.journal.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_journal_description.html')

    def test_change_journal_description_view_valid_post(self):
        # Test the POST request to change_journal_description with valid data
        self.client.force_login(self.user)
        data = {'new_description': 'New Description'}
        response = self.client.post('/change-journal-description/{}/'.format(self.journal.id), data)
        self.assertEqual(response.status_code, 302)  # Assuming you redirect on success
        updated_journal = Journal.objects.get(id=self.journal.id)
        self.assertEqual(updated_journal.journal_description, 'New Description')

    def test_change_journal_description_view_invalid_post(self):
        # Test the POST request to change_journal_description with invalid data
        self.client.force_login(self.user)
        data = {'new_description': ''}
        response = self.client.post('/change-journal-description/{}/'.format(self.journal.id), data)
        self.assertEqual(response.status_code, 200)
        unchanged_journal = Journal.objects.get(id=self.journal.id)
        self.assertEqual(unchanged_journal.journal_description, 'x' * 1000)

    def test_change_journal_description_view_nonexistent_journal(self):
        # Test the change_journal_description view with a nonexistent journal ID
        self.client.force_login(self.user)
        response = self.client.get('/change-journal-description/999/')  # Replace with a nonexistent ID
        self.assertEqual(response.status_code, 404)