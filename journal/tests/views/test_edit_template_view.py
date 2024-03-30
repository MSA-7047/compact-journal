from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from journal.models import Template
from journal.forms import CreateTemplateForm

class EditTemplateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.template = Template.objects.create(
            title='Test Template',
            description='Test Description',
            bio='Test Bio'
        )

    def test_edit_template_view_get(self):
        response = self.client.get(reverse('edit_template', args=[self.template.id]))
        self.assertEqual(response.status_code, 200)  # Check if the view returns 200 OK
        self.assertTemplateUsed(response, 'create_template.html')  # Check if the correct template is used
        self.assertEqual(response.context['template'], self.template)  # Check if the correct template object is passed to the context
        self.assertIsInstance(response.context['form'], CreateTemplateForm)  # Check if the form is an instance of CreateTemplateForm

    def test_edit_template_view_post(self):
        updated_title = 'Updated Title'
        updated_description = 'Updated Description'
        updated_bio = 'Updated Bio'
        post_data = {
            'title': updated_title,
            'description': updated_description,
            'bio': updated_bio
        }
        response = self.client.post(reverse('edit_template', args=[self.template.id]), post_data)
        self.assertEqual(response.status_code, 302)  # Check if the view redirects after successful post
        updated_template = Template.objects.get(id=self.template.id)
        self.assertEqual(updated_template.title, updated_title)  # Check if the template title is updated
        self.assertEqual(updated_template.description, updated_description)  # Check if the template description is updated
        self.assertEqual(updated_template.bio, updated_bio)  # Check if the template bio is updated
