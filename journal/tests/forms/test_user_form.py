from django.test import TestCase
from journal.forms import UserForm
from journal.models import User
from datetime import date

class UserFormTest(TestCase):
    
    def setUp(self):
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': '@johndoe',
            'email': 'johndoe@example.com',
            'dob': date(1990, 1, 1),
            'bio': 'This is a test bio.',
            'location': 'New York',
            'nationality': 'US'
        }

    def test_form_fields(self):
        form = UserForm()
        expected_fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'dob',
            'bio',
            'location',
            'nationality'
        ]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_form_labels(self):
        form = UserForm()
        self.assertEqual(form.fields['dob'].label, 'Date of Birth')
        self.assertEqual(form.fields['nationality'].label, 'Nationality')

    def test_form_widgets(self):
        form = UserForm()
        self.assertEqual(form.fields['dob'].widget.input_type, 'date')

    def test_form_save(self):
        form = UserForm(data=self.user_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.username, '@johndoe')
        self.assertEqual(user.email, 'johndoe@example.com')
        self.assertEqual(user.dob.strftime('%Y-%m-%d'), '1990-01-01')
        self.assertEqual(user.bio, 'This is a test bio.')
        self.assertEqual(user.location, 'New York')
        self.assertEqual(user.nationality, 'US')

