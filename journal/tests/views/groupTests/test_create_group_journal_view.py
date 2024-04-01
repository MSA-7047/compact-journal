from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupEntry, GroupMembership, User

class CreateGroupEntryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email='test@example.com')
        self.group = Group.objects.create(name='Test Group')
        self.group_membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.url = reverse('create_group_journal', kwargs={'group_id': self.group.pk})

    def test_create_group_journal_authenticated_owner(self):
        # Authenticate user
        self.client.force_login(self.user)
        
        # Post valid form data
        form_data = {
            'journal_title': 'Test Journal',
            'journal_description': 'This is a test journal',
            'journal_bio': 'Test journal bio',
            'journal_mood': 'Happy',
        }
        response = self.client.post(self.url, data=form_data)

        # Check if the journal is created and the user is redirected to the group dashboard
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(GroupEntry.objects.count(), 1)
        self.assertEqual(GroupEntry.objects.first().journal_title, 'Test Journal')
        self.assertEqual(GroupEntry.objects.first().last_edited_by, self.user)

    def test_create_group_journal_authenticated_non_owner(self):
        # Create another user who is not the owner of the group
        non_owner_user = User.objects.create(username='@non_owner', password='testpassword', email='non_owner@example.com')
        non_owner_membership = GroupMembership.objects.create(user=non_owner_user, group=self.group)
        
        # Authenticate the non-owner user
        self.client.force_login(non_owner_user)

        # Post form data
        form_data = {
            'journal_title': 'Test Journal',
            'journal_description': 'This is a test journal',
            'journal_bio': 'Test journal bio',
            'journal_mood': 'Happy',
        }
        response = self.client.post(self.url, data=form_data)

        # Check if the non-owner user is redirected and receives an error message
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.pk}))
        self.assertEqual(GroupEntry.objects.count(), 0)

    def test_create_group_journal_unauthenticated_user(self):
        login_url = reverse('log_in')
        # Post form data without authenticating the user
        form_data = {
            'journal_title': 'Test Journal',
            'journal_description': 'This is a test journal',
            'journal_bio': 'Test journal bio',
            'journal_mood': 'Happy',
        }
        response = self.client.post(self.url, data=form_data)

        # Check if the unauthenticated user is redirected to the login page
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, f'{login_url}?next={self.url}')
    
    def test_create_group_journal_invalid_form(self):
        # Authenticate user
        self.client.force_login(self.user)
        
        # Post valid form data
        form_data = {
            'journal_title': '',
            'journal_description': '',
            'journal_bio': 'Test journal bio',
            'journal_mood': 'Happy',
            'private': False, 
        }
        response = self.client.post(self.url, data=form_data)

        # Check if the journal is created and the user is redirected to the group dashboard
        self.assertEqual(response.status_code, 200)  # Redirect status code
        self.assertEqual(GroupEntry.objects.count(), 0)
    
    def test_create_group_journal_get_request_redirection(self):
        # Authenticate user
        self.client.force_login(self.user)
        
        # Make a GET request to the create_group_journal view
        response = self.client.get(self.url)

        # Check if the response redirects to the group dashboard with the correct group_id
        self.assertEqual(response.status_code, 200)  # Redirect status code
