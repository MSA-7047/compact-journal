# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.test.client import Client
# from django.http import HttpRequest
# from django.shortcuts import get_object_or_404
# from journal.models import Template
# from django.contrib.auth import get_user_model

# class DeleteTemplateViewTest(TestCase):
#     def setUp(self):
        # self.client = Client()
        # self.user = get_user_model().objects.create_user(username='testuser', password='password')
#         self.template = Template.objects.create(title='Test Template', description='Test Description', bio='Test Bio', owner=self.user)
#         self.url = reverse('delete_template', args=[self.template.id])

#     def test_delete_template_view_redirect_if_not_logged_in(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 302)  # Redirect code for login

#     def test_delete_template_view_logged_in_user(self):
#         self.client.login(username='testuser', password='password')
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 302)  # Redirect code after successful deletion
#         self.assertFalse(Template.objects.filter(id=self.template.id).exists())  # Ensure template is deleted

#     def test_delete_template_view_template_not_found(self):
#         self.client.login(username='testuser', password='password')
#         non_existent_id = self.template.id + 1
#         non_existent_url = reverse('delete_template', args=[non_existent_id])
#         response = self.client.get(non_existent_url)
#         self.assertEqual(response.status_code, 404)  # Ensure 404 is returned for non-existent template

#     def test_delete_template_view_requires_login(self):
#         # Ensure view redirects to login page when accessed without login
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 302)
#         self.assertIn(reverse('log_in'), response.url)



from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from journal.models import Template, Journal
from journal.views import select_template

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from journal.models import Template, Journal

class TemplateManagementViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)
        # Create a template for the user
        self.template = Template.objects.create(
            title='Test Template',
            description='Description of Test Template',
            bio='Bio content of Test Template',
            owner=self.user
        )

    def test_create_journal_from_template_authenticated_user(self):
        # Get the initial count of journals
        initial_journal_count = Journal.objects.count()
        # Make a POST request to create a journal from the template
        response = self.client.post(reverse('edit_journal'))
        # Check if the response is a redirection
        self.assertEqual(response.status_code, 302)
        # Check if the journal has been created
        self.assertEqual(Journal.objects.count(), initial_journal_count + 1)
        # Check if the redirection is to the edit journal page
        new_journal = Journal.objects.last()
        self.assertRedirects(response, reverse('edit_journal', kwargs={'journalID': new_journal.id}))

class SelectTemplateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)
        self.template1 = Template.objects.create(title='Template 1', description='Description 1', bio='Bio 1', owner=self.user)
        self.template2 = Template.objects.create(title='Template 2', description='Description 2', bio='Bio 2', owner=self.user)

    def test_select_template_view_authenticated_user(self):
        self.client.force_login(self.user)
        url = reverse('select_template')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Ensure successful response
        self.assertTemplateUsed(response, 'select_template.html')  # Ensure correct template used
        self.assertIn('templates', response.context)  # Ensure 'templates' in context
        templates = response.context['templates']
        self.assertEqual(len(templates), 2)  # Ensure correct number of templates retrieved
        self.assertIn(self.template1, templates)  # Ensure first template is in templates
        self.assertIn(self.template2, templates)  # Ensure second template is in templates






