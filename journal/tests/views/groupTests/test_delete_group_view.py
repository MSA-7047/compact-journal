from django.test import TestCase
from django.urls import reverse
from journal.models import Group, GroupMembership, User

class DeleteGroupViewTest(TestCase):
    """Test suite for delete group view"""

    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='testpassword', email="email@gmail.com")
        self.group = Group.objects.create(name='Test Group')
        self.membership = GroupMembership.objects.create(user=self.user, group=self.group, is_owner=True)

    def test_delete_group_authenticated_owner_confirm_yes(self):
        self.client.force_login(self.user)
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url, {'confirmation': 'YES'})

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Group.objects.filter(pk=self.group.pk).exists())

    def test_delete_group_authenticated_owner_confirm_not_yes(self):
        self.client.force_login(self.user)
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url, {'confirmation': 'NO'})

        self.assertEqual(response.status_code, 200) 
        self.assertTrue(Group.objects.filter(pk=self.group.pk).exists())

    def test_delete_group_authenticated_non_owner(self):
        non_owner_user = User.objects.create(username='@non_owner', password='nonownerpassword', email="non_owner@gmail.com")
        GroupMembership.objects.create(user=non_owner_user, group=self.group)

        self.client.force_login(non_owner_user)
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url, {'confirmation': 'YES'})

        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Group.objects.filter(pk=self.group.pk).exists())
        self.assertRedirects(response, reverse('group_dashboard', kwargs={'group_id': self.group.pk}))

    def test_delete_group_unauthenticated_user(self):
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url, {'confirmation': 'YES'})

        self.assertRedirects(response, f'/log_in/?next=/groups/{self.group.pk}/delete')
        self.assertTrue(Group.objects.filter(pk=self.group.pk).exists())
    
    def test_delete_group_correct_redirection(self):
        self.client.force_login(self.user)
        url = reverse('delete_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
    
    def test_delete_group_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_group', kwargs={'group_id': self.group.group_id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_account.html')
