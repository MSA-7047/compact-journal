from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupEntry, GroupMembership, User

class EditGroupJournalViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email='test@example.com')
        self.group = Group.objects.create(name='Test Group')
        self.group_membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.group_journal = GroupEntry.objects.create(title='Test Journal', summary='This is a test journal', content='Test journal bio', mood='Happy', last_edited_by=self.user, owner=self.group)
        self.url = reverse('edit_group_journal', kwargs={'group_id': self.group.pk, 'journal_id': self.group_journal.pk})

    def test_edit_group_journal_authenticated_owner(self):
        # Authenticate user
        self.client.force_login(self.user)
        
        # Post valid form data
        form_data = {
            'title': 'Updated Test Journal',
            'summary': 'This is a new test journal',
            'content': 'Test journal bio part 2',
            'mood': 'Angry',
        }
        response = self.client.post(self.url, data=form_data)

        # Check if the journal is created and the user is redirected to the group dashboard
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(GroupEntry.objects.first().title, 'Updated Test Journal')
        self.assertEqual(GroupEntry.objects.first().last_edited_by, self.user)

    def test_edit_group_journal_authenticated_non_owner(self):
        # Create another user who is not the owner of the group
        non_owner_user = User.objects.create(username='@non_owner', password='testpassword', email='non_owner@example.com')
        non_owner_membership = GroupMembership.objects.create(user=non_owner_user, group=self.group)
        
        # Authenticate the non-owner user
        self.client.force_login(non_owner_user)

        # Post form data
        form_data = {
            'title': 'Updated Test Journal',
            'summary': 'This is a new test journal',
            'content': 'Test journal bio part 2',
            'mood': 'Angry',
        }
        
        response = self.client.post(self.url, data=form_data)

        # Check if the non-owner user is redirected and receives an error message
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(GroupEntry.objects.first().title, 'Updated Test Journal')
        self.assertEqual(GroupEntry.objects.first().last_edited_by, non_owner_user)

    def test_edit_group_journal_unauthenticated_user(self):
        login_url = reverse('log_in')
        # Post form data without authenticating the user
        form_data = {
            'title': 'Updated Test Journal',
            'summary': 'This is a new test journal',
            'content': 'Test journal bio part 2',
            'mood': 'Angry',
        }
        response = self.client.post(self.url, data=form_data)

        # Check if the unauthenticated user is redirected to the login page
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, f'{login_url}?next={self.url}')
    
    def test_edit_group_journal_invalid_form(self):
        # Authenticate user
        self.client.force_login(self.user)
        
        # Post valid form data
        form_data = {
            'title': '',
            'summary': '',
            'content': 'Test journal bio',
            'mood': 'Angry',
        }
        response = self.client.post(self.url, data=form_data)

        # Check if the journal is created and the user is redirected to the group dashboard
        self.assertEqual(response.status_code, 200)  # Redirect status code

    def test_create_group_journal_get_request_redirection(self):
        # Authenticate user
        self.client.force_login(self.user)
        
        # Make a GET request to the create_group_journal view
        response = self.client.get(self.url)

        # Check if the response redirects to the group dashboard with the correct group_id
        self.assertEqual(response.status_code, 200)  # Redirect status code