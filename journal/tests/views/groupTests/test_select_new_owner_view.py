from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupMembership, User, Notification


class SelectNewOwnerViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email="email@gmail.com")
        self.user2 = User.objects.create(username='@testuser2', password='testpassword', email="email2@gmail.com")
        self.group = Group.objects.create(name='Test Group')
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.membership2 = GroupMembership.objects.create(user=self.user2, group=self.group)
        self.url = reverse('select_new_owner', kwargs={'group_id': self.group.pk})
    
    def test_view_redirect_non_owner(self):
        # Create another user who is not the owner of the group
        self.client.force_login(self.user2)

        response = self.client.get(self.url)

        # Check if the view redirects to the group dashboard
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.pk}))

    def test_view_render_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        # Check if the view renders the form correctly
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['group'], self.group)
        self.assertEqual(response.context['user'], self.user)

    def test_select_new_owner(self):
        self.client.force_login(self.user)

        # Post form data
        form_data = {
            'new_owner': self.user2.pk,
        }
        response = self.client.post(self.url, form_data)

        # Check if the view redirects to the dashboard after selecting new owner
        self.assertRedirects(response, reverse('dashboard'))

        # Check if the group membership is updated correctly
        self.assertFalse(GroupMembership.objects.filter(group=self.group, user=self.user, is_owner=True).exists())
        self.assertTrue(GroupMembership.objects.filter(group=self.group, user=self.user2, is_owner=True).exists())
        self.assertTrue(Notification.objects.filter(user=self.user2, notification_type="group"))

    def test_select_new_owner_invalid(self):
        self.client.force_login(self.user)

        # Post form data
        form_data = {
            'new_owner': '@User1',
        }
        
        response = self.client.post(self.url, form_data)

        # Check if the view redirects to the dashboard after selecting new owner
        self.assertEqual(response.status_code, 200)

        # Check if the form errors are present in the response context
        form_errors = response.context['form'].errors
        self.assertTrue(form_errors)  # Assert that form errors are not empty