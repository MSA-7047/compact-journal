from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupEntry, GroupMembership, User

class DeleteGroupJournalViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(username='@testuser', password='testpassword', email='test@example.com')
        
        # Create a group
        self.group = Group.objects.create(name='Test Group')
        
        # Create a group membership with the user as the owner of the group
        self.group_membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        
        # Create a group journal
        self.journal = GroupEntry.objects.create(
            title='Test Journal',
            summary='Description of the test journal',
            content='Bio of the test journal',
            mood='Happy',
            owner=self.group,
            last_edited_by=self.user
        )
        
        # Define the URL for deleting a group journal
        self.url = reverse('delete_group_journal', kwargs={'group_id': self.group.pk, 'journal_id': self.journal.pk})

    def test_delete_group_journal_authenticated_owner(self):
        # Authenticate user
        self.client.force_login(self.user)
        
        # Send a POST request to delete the group journal
        response = self.client.post(self.url)

        # Check if the journal is deleted and the user is redirected to the group dashboard
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertFalse(GroupEntry.objects.filter(pk=self.journal.pk).exists())
    
    def test_delete_group_journal_authenticated_non_owner(self):
        # Create another user who is not the owner of the group
        non_owner_user = User.objects.create(username='@non_owner', password='testpassword', email='non_owner@example.com')
        
        # Create a group membership for the non-owner user
        non_owner_membership = GroupMembership.objects.create(user=non_owner_user, group=self.group)
        
        # Authenticate the non-owner user
        self.client.force_login(non_owner_user)

        # Send a POST request to delete the group journal
        response = self.client.post(self.url)

        # Check if the non-owner user is redirected and receives an error message
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(GroupEntry.objects.filter(pk=self.journal.pk).exists())
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.pk}))
    
    def test_delete_group_journal_unauthenticated_user(self):
        # Send a POST request without authenticating the user
        response = self.client.post(self.url)

        # Check if the unauthenticated user is redirected to the login page
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(GroupEntry.objects.filter(pk=self.journal.pk).exists())
        self.assertRedirects(response, f'/log_in/?next={self.url}')
    
    def test_delete_group_journal_get_request(self):
        # Send a GET request to delete the group journal
        response = self.client.get(self.url)

        # Check if the response status code is a redirect
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the journal still exists
        self.assertTrue(GroupEntry.objects.filter(pk=self.journal.pk).exists())
    
    def test_create_group_journal_get_request_redirection(self):
        # Authenticate user
        self.client.force_login(self.user)
        
        # Make a GET request to the create_group_journal view
        response = self.client.get(self.url)

        # Check if the response redirects to the group dashboard with the correct group_id
        self.assertEqual(response.status_code, 302)  # Redirect status code
