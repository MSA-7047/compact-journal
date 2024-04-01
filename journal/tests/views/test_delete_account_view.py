from django.test import TestCase, Client
from django.urls import reverse
from journal.models import User

class DeleteAccountViewTest(TestCase):

    fixtures = [
        'journal/tests/fixtures/default_user.json',]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username='@johndoe', password='Password123')

    def test_delete_account_POST_valid_form(self):
        response = self.client.post(reverse('delete_account'), {'confirmation': 'YES'})
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is received
        self.assertFalse(User.objects.filter(username='@johndoe').exists())  # Check if user is deleted
        # Add more assertions as needed

    def test_delete_account_POST_invalid_form(self):
        response = self.client.post(reverse('delete_account'), {'confirmation': 'Invalid Form'})
        self.assertEqual(response.status_code, 200)  # Check if form submission does not redirect
        self.assertTrue(User.objects.filter(username='@johndoe').exists())  # Check if user still exists
        # Add more assertions as needed

    def test_delete_account_GET(self):
        response = self.client.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 200)  # Check if success status code is received
        self.assertTemplateUsed(response, 'delete_account.html')  # Check if correct template is used
        # Add more assertions as needed