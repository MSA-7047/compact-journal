from django.test import TestCase
from django.urls import reverse
from journal.models import GroupJournal, GroupMembership, Group, User
from journal.forms import CreateGroupJournalForm

class CreateGroupJournalViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.group = Group.objects.create()
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        
        self.url = reverse('create_journal_view')
        self.form_input = {
            'journal_title': 'My 21st birthday',
            'journal_description': 'x' * 1000,
            'journal_bio': 'x' * 10000,
            'journal_mood': 'Happy',
            'private': True,  # Assuming this field exists in the form
        }

    def test_create_journal_view_get(self):
        """
        Test if the create journal view returns the correct status code and uses
        the correct template when accessed via GET request.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_journal.html')

    def test_create_journal_view_post_valid(self):
        """
        Test if the create journal view creates a new journal object with valid data.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=self.form_input)
        self.assertEqual(response.status_code, 302)  # Redirects upon successful creation
        self.assertTrue(GroupJournal.objects.filter(journal_title=self.form_input['journal_title']).exists())

    def test_create_journal_view_post_invalid(self):
        """
        Test if the create journal view handles invalid form data properly.
        """
        self.client.force_login(self.user)
        # Modify form input to make it invalid
        invalid_form_input = self.form_input.copy()
        invalid_form_input['journal_title'] = ''  # Making journal_title empty to trigger form validation error
        response = self.client.post(self.url, data=invalid_form_input)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page with errors
        self.assertFalse(GroupJournal.objects.filter(journal_title='').exists())

    def test_create_journal_view_not_owner(self):
        """
        Test if the create journal view returns forbidden response for non-owners.
        """
        non_owner = User.objects.create()  # Create a non-owner user
        self.client.force_login(non_owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)  # Should return forbidden response

    def test_create_journal_view_not_authenticated(self):
        """
        Test if the create journal view redirects to login page for unauthenticated users.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

    # Add more test cases as needed
