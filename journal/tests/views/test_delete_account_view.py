from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from journal.forms import ConfirmAccountDeleteForm

class DeleteAccountViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_delete_account_successful(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('delete_account')
        data = {'confirmation': 'YES'}

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(User.objects.filter(username='testuser').exists())