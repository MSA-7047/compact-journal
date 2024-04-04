from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupEntry, GroupMembership, User

class EditGroupEntryViewTest(TestCase):
    """Test suite for edit group entry view"""

    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email='test@example.com')
        self.group = Group.objects.create(name='Test Group')
        self.group_membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)
        self.group_journal = GroupEntry.objects.create(title='Test Journal', summary='This is a test journal', content='Test journal bio', mood='Happy', last_edited_by=self.user, owner=self.group)
        self.url = reverse('edit_group_journal', kwargs={'group_id': self.group.pk, 'journal_id': self.group_journal.pk})

    def test_edit_group_journal_authenticated_owner(self):
        self.client.force_login(self.user)
        form_data = {
            'title': 'Updated Test Journal',
            'summary': 'This is a new test journal',
            'content': 'Test journal bio part 2',
            'mood': 'Angry',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(GroupEntry.objects.first().title, 'Updated Test Journal')
        self.assertEqual(GroupEntry.objects.first().last_edited_by, self.user)

    def test_edit_group_journal_authenticated_non_owner(self):
        non_owner_user = User.objects.create(username='@non_owner', password='testpassword', email='non_owner@example.com')
        GroupMembership.objects.create(user=non_owner_user, group=self.group)
        form_data = {
            'title': 'Updated Test Journal',
            'summary': 'This is a new test journal',
            'content': 'Test journal bio part 2',
            'mood': 'Angry',
        }

        self.client.force_login(non_owner_user)
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(GroupEntry.objects.first().title, 'Updated Test Journal')
        self.assertEqual(GroupEntry.objects.first().last_edited_by, non_owner_user)

    def test_edit_group_journal_unauthenticated_user(self):
        login_url = reverse('log_in')
        form_data = {
            'title': 'Updated Test Journal',
            'summary': 'This is a new test journal',
            'content': 'Test journal bio part 2',
            'mood': 'Angry',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, f'{login_url}?next={self.url}')
    
    def test_edit_group_journal_invalid_form(self):
        self.client.force_login(self.user)
        
        # Post valid form data
        form_data = {
            'title': '',
            'summary': '',
            'content': 'Test journal bio',
            'mood': 'Angry',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)

    def test_create_group_journal_get_request_redirection(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)