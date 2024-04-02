from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupMembership, GroupEntry, User

class ViewGroupEntryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email='test@example.com')
        self.group = Group.objects.create(name='Test Group')
        self.journal1 = GroupEntry.objects.create(title='Journal 1', summary='Description 1', content='Bio 1', mood='Happy', owner=self.group)
        self.journal2 = GroupEntry.objects.create(title='Journal 2', summary='Description 2', content='Bio 2', mood='Sad', owner=self.group)
        self.url = reverse('view_group_journals', kwargs={'group_id': self.group.pk})
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group)

    def test_view_group_journals_authenticated_user(self):
        # Authenticate user
        self.client.force_login(self.user)
        
        # Access the view
        response = self.client.get(self.url)

        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check if both journals are present in the response context
        self.assertIn(self.journal1, response.context['group_journals'])
        self.assertIn(self.journal2, response.context['group_journals'])

    def test_view_group_journals_unauthenticated_user(self):
        # Access the view without authenticating the user
        response = self.client.get(self.url)

        # Check response status code
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the user is redirected to the login page
        self.assertRedirects(response, f'/log_in/?next={self.url}')
