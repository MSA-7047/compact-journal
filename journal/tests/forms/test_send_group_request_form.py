from django.test import TestCase
from journal.models import User
from journal.forms import SendGroupRequestForm

class SendGroupRequestFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_form_with_current_user(self):
        """Test form initialization with current user."""
        # Create some friends for the user
        friend1 = User.objects.create_user(username='friend1', email='friend1@example.com', password='password')
        friend2 = User.objects.create_user(username='friend2', email='friend2@example.com', password='password')
        self.user.friends.add(friend1, friend2)

        # Initialize form with current user
        form = SendGroupRequestForm(currentUser=self.user)
        # Check if the queryset for recipient field is set to the friends of the current user
        self.assertQuerysetEqual(form.fields['recipient'].queryset, self.user.friends.all(), transform=lambda x: x)

    def test_form_with_empty_queryset(self):
        """Test form initialization with empty queryset."""
        # Initialize form with empty queryset
        form = SendGroupRequestForm(currentUser=self.user)

        # Check if the queryset for recipient field is empty
        self.assertQuerysetEqual(form.fields['recipient'].queryset, User.objects.none(), transform=lambda x: x)

    def test_form_field_label(self):
        """Test form field label."""
        form = SendGroupRequestForm()
        self.assertEqual(form.fields['recipient'].label, 'Select User')
