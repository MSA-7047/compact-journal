# tests.py
from django.test import TestCase
from journal.models import User, Group, GroupMembership
from journal.forms import SelectNewOwnerForm

class SelectNewOwnerFormTest(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json',
                'journal/tests/fixtures/other_users.json']
    
    def setUp(self):
        self.user1 = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.user3 = User.objects.get(username='@petrapickles')
        self.group = Group.objects.create(name='Test Group')

        self.owner_membership = GroupMembership.objects.create(user=self.user1, group=self.group, is_owner=True)
        self.member_membership = GroupMembership.objects.create(user=self.user2, group=self.group)
        self.member_membership = GroupMembership.objects.create(user=self.user3, group=self.group)

    def test_form_queryset_filtering(self):
        # Test if the form correctly filters users based on group memberships excluding the current user.
        form = SelectNewOwnerForm(group=self.group, current_user=self.user1)
        self.assertEqual(form.fields['new_owner'].queryset.count(), 2)
        self.assertIn(self.user2, form.fields['new_owner'].queryset)
        self.assertIn(self.user3, form.fields['new_owner'].queryset)
        self.assertNotIn(self.user1, form.fields['new_owner'].queryset)

    def test_form_valid_submission(self):
        form_data = {'new_owner': self.user2.id}
        form = SelectNewOwnerForm(data=form_data, group=self.group, current_user=self.user1)
        self.assertTrue(form.is_valid())

    def test_form_invalid_submission(self):
        form_data = {}  # Missing 'new_owner' field.
        form = SelectNewOwnerForm(data=form_data, group=self.group)
        self.assertFalse(form.is_valid())
        self.assertIn('new_owner', form.errors)
        self.assertEqual(form.errors['new_owner'], ['This field is required.'])

    def test_current_user_not_in_queryset(self):
        form = SelectNewOwnerForm(group=self.group, current_user=self.user1)
        self.assertNotIn(self.user1, form.fields['new_owner'].queryset) # Check that user cannot choose himself as new owner again.
