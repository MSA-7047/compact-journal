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
        form = SendFriendRequestForm()
        self.assertTrue('recipient' in form.fields)
    
    def test_form_doesnt_accept_blank(self):
        form_data = {'recipient': ''}
        form = SendFriendRequestForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_existing_friend(self):
        self.user.friends.set([self.friend2])
        form_data = {'recipient': self.friend2.username}
        form = SendFriendRequestForm(data=form_data)
        form.is_valid()

        self.assertFalse(form.check_user(user=self.user))
        self.assertIn('recipient', form.errors)
        self.assertEqual(form.errors['recipient'], ['User is already your friend'])

    def test_form_with_self_request(self):
        self.user.friends.set([self.friend2])
        form_data = {'recipient': self.user.username}
        form = SendFriendRequestForm(data=form_data)
        form.is_valid()

        self.assertFalse(form.check_user(user=self.user))
        self.assertIn('recipient', form.errors)
        self.assertEqual(form.errors['recipient'], ['Cannot request yourself'])

    def test_form_with_non_existing_user(self):
        form_data = {'recipient': 'non_existing_user'}
        form = SendFriendRequestForm(data=form_data)
        form.is_valid()

        self.assertFalse(form.check_user(user=self.user))
        self.assertIn('recipient', form.errors)
        self.assertEqual(form.errors['recipient'], ["This user doesn't exist"])

    def test_valid_form(self):
        form_data = {'recipient': self.friend2.username}
        form = SendFriendRequestForm(data=form_data)
        form.is_valid()

        self.assertTrue(form.check_user(user=self.user))
        self.assertEqual(len(form.errors), 0)
    
    def test_form_field_label(self):
        """Test form field label."""
        form = SendFriendRequestForm()
        self.assertEqual(form.fields['recipient'].label, 'Select User')
    


