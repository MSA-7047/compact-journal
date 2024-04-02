from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupRequest, GroupMembership, User

class GroupViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user1 = User.objects.create(username='@testuser', password='password', email="email@email.org")
        self.user2 = User.objects.create(username='@testuser2', password='password', email="email2@email.org")
        
        # Create groups
        self.group1 = Group.objects.create(name='Group 1')
        self.group2 = Group.objects.create(name='Group 2')
        
        self.membership1 = GroupMembership.objects.create(user=self.user1, group=self.group1, is_owner=True)
        self.membership2 = GroupMembership.objects.create(user=self.user2, group=self.group2, is_owner=True)

        # Create a group request for the user
        self.group_request = GroupRequest.objects.create(sender=self.user2, recipient=self.user1, group=self.group2, status='Pending')

    def test_group_view_with_authenticated_user(self):
        # Log in the user
        self.client.force_login(self.user1)
        
        # Access the group view
        response = self.client.get(reverse('groups'))
        
        # Check if the user is in the response context
        self.assertEqual(response.context['user'], self.user1)
        
        # Check if the group request is in the response context
        self.assertQuerysetEqual(response.context['group_requests'], [self.group_request])


    def test_group_view_with_unauthenticated_user(self):
        # Log out the user
        self.client.logout()
        
        # Access the group view
        response = self.client.get(reverse('groups'))
        
        # Check if the user is redirected to the login page
        self.assertRedirects(response, '/log_in/?next=/groups/')  # Adjust the redirect URL if needed