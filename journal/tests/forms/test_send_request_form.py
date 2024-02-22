from django.test import TestCase
from journal.models import User
from journal.forms import SendFriendRequestForm

class SendFriendRequestFormTest(TestCase):
    fixtures = ['journal/tests/fixtures/default_user.json',
                'journal/tests/fixtures/other_users.json']

    def setUp(self):
        # Create a user with some friends for testing
        self.user = User.objects.get(username='@johndoe')
        self.friend1 = User.objects.get(username='@janedoe')
        self.friend2 = User.objects.get(username="@petrapickles")

    def test_form_has_required_fields(self):
        form = SendFriendRequestForm(user=self.user)
        self.assertTrue('recipient' in form.fields)

    def test_form_validation_for_valid_data(self):
        # Test the form validation for a valid recipient
        recipient = User.objects.create_user(username='valid_recipient', password='password')
        form_data = {'recipient': recipient.id}
        form = SendFriendRequestForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_validation_for_same_user_as_recipient(self):
        self.user.friends.set([self.friend1, self.friend2])
        form_data = {'recipient': self.user.id}
        form = SendFriendRequestForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('recipient', form.errors)

    def test_form_validation_for_friend_as_recipient(self):
        self.user.friends.set([self.friend1, self.friend2])
        form_data = {'recipient': self.friend1.id}
        form = SendFriendRequestForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('recipient', form.errors)

    def test_form_queryset_excludes_friends(self):
        self.user.friends.set([self.friend1, self.friend2])
        form = SendFriendRequestForm(user=self.user)
        queryset = form.fields['recipient'].queryset

        # Ensure that friends and user are excluded from the queryset
        self.assertNotIn(self.user, queryset)
        self.assertNotIn(self.friend1, queryset)
        self.assertNotIn(self.friend2, queryset)

    def test_form_queryset_includes_other_users(self):
        form = SendFriendRequestForm(user=self.user)
        queryset = form.fields['recipient'].queryset
        # Ensure that other users are included in the queryset
        all_users_except_current = User.objects.exclude(id=self.user.id)
        for other_user in all_users_except_current:
            self.assertIn(other_user, queryset)