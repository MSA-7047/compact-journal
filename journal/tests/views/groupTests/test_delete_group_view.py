from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupMembership, User

class DeleteGroupViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email="email@gmail.com")
        self.group = Group.objects.create(name='Test Group')
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)

    def test_delete_group_authenticated_owner_confirm_yes(self):
        """Test deleting a group by an authenticated owner with confirmation 'YES'."""
        self.client.force_login(self.user)
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url, {'confirmation': 'YES'})

        # Check if the group is deleted and user redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertFalse(Group.objects.filter(pk=self.group.pk).exists())

    def test_delete_group_authenticated_owner_confirm_no(self):
        """Test deleting a group by an authenticated owner with confirmation other than 'YES'."""
        self.client.force_login(self.user)
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url, {'confirmation': 'NO'})

        # Check if the group is not deleted and user redirected
        self.assertEqual(response.status_code, 200)  # Redirect status code
        self.assertTrue(Group.objects.filter(pk=self.group.pk).exists())

    def test_delete_group_authenticated_non_owner(self):
        """Test deleting a group by an authenticated non-owner."""
        non_owner_user = User.objects.create(username='@non_owner', password='nonownerpassword', email="non_owner@gmail.com")
        membership = GroupMembership.objects.create(user=non_owner_user, group=self.group)
        self.client.force_login(non_owner_user)
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url, {'confirmation': 'YES'})

        # Check if the group is not deleted and user redirected with error message
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Group.objects.filter(pk=self.group.pk).exists())
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.pk}))

    def test_delete_group_unauthenticated_user(self):
        """Test deleting a group by an unauthenticated user."""
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url, {'confirmation': 'YES'})

        # Check if the user is redirected to the login page
        self.assertRedirects(response, f'/log_in/?next=/groups/{self.group.pk}/delete')

        # Check if the group is not deleted
        self.assertTrue(Group.objects.filter(pk=self.group.pk).exists())
    
    def test_delete_group_correct_redirection(self):
        """Test for checking if the redirect is correct."""
        self.client.force_login(self.user)
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url)

        # Check if the group is not deleted and user redirected
        self.assertEqual(response.status_code, 200)  # Redirect status code
    
    def test_delete_group_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_group', kwargs={'group_id': self.group.group_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_account.html')
