from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupEntry, GroupMembership, User

class DeleteGroupEntryViewTest(TestCase):
    """Test suite for the deleting group entry view"""

    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email='test@example.com')
        self.group = Group.objects.create(name='Test Group')
        self.group_membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.journal = GroupEntry.objects.create(
            title='Test Journal',
            summary='Description of the test journal',
            content='Bio of the test journal',
            mood='Happy',
            owner=self.group,
            last_edited_by=self.user
        )
        
        self.url = reverse('delete_group_journal', kwargs={'group_id': self.group.pk, 'journal_id': self.journal.pk})

    def test_delete_group_journal_authenticated_owner(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302) 
        self.assertFalse(GroupEntry.objects.filter(pk=self.journal.pk).exists())
    
    def test_delete_group_journal_non_owner_rejected(self):
        non_owner_user = User.objects.create(username='@non_owner', password='testpassword', email='non_owner@example.com')
        GroupMembership.objects.create(user=non_owner_user, group=self.group)
        
        self.client.force_login(non_owner_user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302) 
        self.assertTrue(GroupEntry.objects.filter(pk=self.journal.pk).exists())
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.pk}))
    
    def test_delete_group_journal_unauthenticated_user(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(GroupEntry.objects.filter(pk=self.journal.pk).exists())
        self.assertRedirects(response, f'/log_in/?next={self.url}')
    
    def test_create_group_journal_get_request_redirection(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
    
    def test_delete_group_journal_referer_group_dashboard(self):
        self.client.force_login(self.user)
        referer_url = reverse('group_dashboard', kwargs={'group_id': self.group.pk})
        response = self.client.post(self.url, HTTP_REFERER=referer_url)

        self.assertRedirects(response, referer_url)

    def test_delete_group_journal_referer_view_group_journals(self):
        self.client.force_login(self.user)
        referer_url = reverse('view_group_journals', kwargs={'group_id': self.group.pk})
        response = self.client.post(self.url, HTTP_REFERER=referer_url)

        self.assertRedirects(response, referer_url)

    def test_delete_group_journal_referer_other_page(self):
        self.client.force_login(self.user)
        referer_url = ''
        response = self.client.post(self.url, HTTP_REFERER=referer_url)

        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.pk}))

