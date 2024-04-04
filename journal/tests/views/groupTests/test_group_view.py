from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupRequest, GroupMembership, User

class GroupViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='@testuser', password='password', email="email@email.org")
        self.user2 = User.objects.create(username='@testuser2', password='password', email="email2@email.org")
        self.group = Group.objects.create(name='Group')
        self.membership = GroupMembership.objects.create(user=self.user2, group=self.group, is_owner=True)
        self.group_request = GroupRequest.objects.create(sender=self.user2, recipient=self.user1, group=self.group, status='Pending')

    def test_group_view_with_authenticated_user(self):
        self.client.force_login(self.user1)        
        response = self.client.get(reverse('groups'))
        
        self.assertEqual(response.context['user'], self.user1)        
        self.assertQuerysetEqual(response.context['group_requests'], [self.group_request])


    def test_group_view_with_unauthenticated_user(self):
        self.client.logout()        
        response = self.client.get(reverse('groups'))
        
        self.assertRedirects(response, '/log_in/?next=/groups/')