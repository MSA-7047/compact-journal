from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupRequest, GroupMembership, User

class GroupRequestAcceptanceTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='@testuser', password='Password123', email="example@hotmail.com")
        self.user2 = User.objects.create_user(username='@testuser2', password='Password123', email="example2@hotmail.com")

        # Create a test group
        self.group = Group.objects.create(name='TestGroup')

        # Create a group request
        self.group_request = GroupRequest.objects.create(
            sender=self.user,
            recipient=self.user2,
            group=self.group
        )

    def test_accept_group_request(self):
        # Ensure the group request is not accepted initially
        self.assertFalse(self.group_request.is_accepted)

        # Log in as the test user (if necessary)
        self.client.login(username='testuser', password='password')

        # Send a POST request to the accept_group_invitation view
        response = self.client.post(reverse('accept_group_invitation', args=[self.group_request.id]))

        # Check that the response redirects to the correct page (e.g., group page)
        self.assertRedirects(response, reverse('group'))

        # Reload the group request from the database
        self.group_request.refresh_from_db()

        # Check that the group request is now accepted
        self.assertTrue(self.group_request.is_accepted)

        # Check that a GroupMembership object is created for the user and group
        group_membership = GroupMembership.objects.filter(user=self.user, group=self.group).exists()
        self.assertTrue(group_membership)