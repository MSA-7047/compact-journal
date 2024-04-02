from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from journal.models import Template
from journal.forms import CreateTemplateForm
from django.contrib.auth import get_user_model


class CreateTemplateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')

    def test_get_request(self):
        response = self.client.get(reverse('create_template'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_template.html')
        self.assertIsInstance(response.context['form'], CreateTemplateForm)

    def test_post_request_valid_data(self):
        data = {
            'title': 'Test Template',
            'description': 'Test description',
            'bio': 'Test bio',
        }
        response = self.client.post(reverse('create_template'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Template.objects.filter(title='Test Template').exists())

    def test_post_request_invalid_data(self):
        data = {} 
        response = self.client.post(reverse('create_template'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'This field is required.')

