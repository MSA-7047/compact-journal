from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Entry, User





class ChangeJournalBioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.journal = Entry.objects.create(

            journal_title = 'My 21st birthday',
            journal_description= 'x' * 1000,
            journal_bio= 'x' * 10000,
            journal_mood= 'Happy'
        )

    def test_change_journal_bio_view_get(self):
        # Test the GET request to the change_journal_bio view
        self.client.force_login(self.user)
        response = self.client.get('/change-journal-bio/{}/'.format(self.journal.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_journal_bio.html')

    def test_change_journal_bio_view_valid_post(self):
        # Test the POST request to change_journal_bio with valid data
        self.client.force_login(self.user)
        data = {'new_bio': 'New Bio'}
        response = self.client.post('/change-journal-bio/{}/'.format(self.journal.id), data)
        self.assertEqual(response.status_code, 302)  # Assuming you redirect on success
        updated_journal = Entry.objects.get(id=self.journal.id)
        self.assertEqual(updated_journal.journal_bio, 'New Bio')

    def test_change_journal_bio_view_invalid_post(self):
        # Test the POST request to change_journal_bio with invalid data
        self.client.force_login(self.user)
        data = {'new_bio': ''}
        response = self.client.post('/change-journal-bio/{}/'.format(self.journal.id), data)
        self.assertEqual(response.status_code, 200)
        unchanged_journal = Entry.objects.get(id=self.journal.id)
        self.assertEqual(unchanged_journal.journal_bio, 'x' * 10000)

    def test_change_journal_bio_view_nonexistent_journal(self):
        # Test the change_journal_bio view with a nonexistent journal ID
        self.client.force_login(self.user)
        response = self.client.get('/change-journal-bio/999/')  # Replace with a nonexistent ID
        self.assertEqual(response.status_code, 404)


#alternative implementation
# class CreateJournalViewTestCase(TestCase):

#     def setUp(self):
#         self.client = Client()

#         # Create a user
#         self.user1 = User.objects.create(username='USER1', email='guacamole@gmail.com', password='Password123')
#         self.user2 = User.objects.create(username='USER2', email='cheese@gmail.com', password='Password456')

#         self.url = reverse('change_journal_title')
#         self.form_input = {

#             'journal_title': 'My 21st birthday',
#             'journal_description': 'x' * 1000,
#             'journal_bio': 'x' * 10000,
#             'journal_mood': 'Happy',
#         }

#     def test_create_journal_view_url(self):
#         self.assertEqual(self.url,'/change_journal_title/')

    
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