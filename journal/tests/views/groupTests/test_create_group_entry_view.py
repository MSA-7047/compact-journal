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
        self.client.force_login(self.user)
        form_data = {
            'title': 'Test Journal',
            'summary': 'This is a test journal',
            'content': 'Test journal bio',
            'mood': 'Happy',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(GroupEntry.objects.count(), 1)
        self.assertEqual(GroupEntry.objects.first().title, 'Test Journal')
        self.assertEqual(GroupEntry.objects.first().last_edited_by, self.user)

    def test_create_group_journal_authenticated_non_owner(self):
        non_owner_user = User.objects.create(username='@non_owner', password='testpassword', email='non_owner@example.com')
        GroupMembership.objects.create(user=non_owner_user, group=self.group)
        
        self.client.force_login(non_owner_user)
        form_data = {
            'title': 'Test Journal',
            'summary': 'This is a test journal',
            'content': 'Test journal bio',
            'mood': 'Happy',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.pk}))
        self.assertEqual(GroupEntry.objects.count(), 0)

    def test_create_group_journal_unauthenticated_user(self):
        login_url = reverse('log_in')
        form_data = {
            'jtitle': 'Test Journal',
            'description': 'This is a test journal',
            'content': 'Test journal bio',
            'mood': 'Happy',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{login_url}?next={self.url}')
    
    def test_create_group_journal_invalid_form(self):
        self.client.force_login(self.user)
        form_data = {
            'title': '',
            'summary': '',
            'content': 'Test journal bio',
            'mood': 'Happy',
            'private': False, 
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(GroupEntry.objects.count(), 0)
    
    def test_create_group_journal_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
