from django.test import TestCase
from django.urls import reverse
from journal.models import Template, Journal, Entry, User
from journal.forms import CreateTemplateForm

class TemplateViewsTestCase(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):

        self.user = User.objects.get(username='@johndoe')
        self.client.login(username='@johndoe', password='Password123')

        self.journal = Journal.objects.create(title="Test Journal", summary="testing purposes", private=False, owner=self.user)

        # Create some sample templates
        self.template = Template.objects.create(
            title='Test Template',
            description='Test Template Description',
            bio='Test Template Content',
            owner=self.user
        )

    def test_create_template_view(self):
        response = self.client.get(reverse('create_template', args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('create_template', args=[self.journal.id]), {
            'title': 'New Template',
            'description': 'New Template Description',
            'bio': 'New Template Content'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission
        self.assertTrue(Template.objects.filter(title='New Template').exists())

    def test_create_invalid_template_view(self):
        response = self.client.get(reverse('create_template', args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('create_template', args=[self.journal.id]), {
            'title': '',
            'description': '',
            'bio': ''
        })
        self.assertEqual(response.status_code, 200) 
        self.assertFalse(Template.objects.filter(title='').exists())

    def test_select_template_view(self):
        response = self.client.get(reverse('select_template', args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'select_template.html')

    def test_delete_template_view(self):
        response = self.client.post(reverse('delete_template', args=[self.template.id, self.journal.id]))
        self.assertEqual(response.status_code, 302) 

        # Ensure the template is deleted
        self.assertFalse(Template.objects.filter(id=self.template.id).exists())

    def test_create_journal_from_template_view(self):
        response = self.client.post(reverse('create_journal_with_template', args=[self.template.id, self.journal.id]))
        self.assertEqual(response.status_code, 302)  

        # Ensure an entry is created
        self.assertTrue(Entry.objects.filter(title=self.template.title).exists())

    def test_edit_template_view(self):
        response = self.client.get(reverse('edit_template', args=[self.template.id, self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_template.html')

        response = self.client.post(reverse('edit_template', args=[self.template.id, self.journal.id]), {
            'title': 'Updated Template',
            'description': 'Updated Template Description',
            'bio': 'Updated Template Content'
        })
        self.assertEqual(response.status_code, 302) 

        # Ensure the template is updated
        self.template.refresh_from_db()
        self.assertEqual(self.template.title, 'Updated Template')





