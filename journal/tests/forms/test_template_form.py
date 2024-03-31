from django.test import TestCase
from journal.models import Template
from journal.forms import CreateTemplateForm

class CreateTemplateFormTest(TestCase):

    def test_form_fields(self):
        form = CreateTemplateForm()
        expected_fields = ['title', 'description', 'bio']
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_bio_field_not_required(self):
        form = CreateTemplateForm()
        self.assertFalse(form.fields['bio'].required)

    def test_form_save(self):
        form_data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'bio': 'Test Bio'
        }
        form = CreateTemplateForm(data=form_data)
        self.assertTrue(form.is_valid())
        template = form.save(commit=False)
        self.assertEqual(template.title, 'Test Title')
        self.assertEqual(template.description, 'Test Description')
        self.assertEqual(template.bio, 'Test Bio')

    def test_form_save_without_bio(self):
        form_data = {
            'title': 'Test Title',
            'description': 'Test Description'
        }
        form = CreateTemplateForm(data=form_data)
        self.assertTrue(form.is_valid())
        template = form.save(commit=False)
        self.assertEqual(template.title, 'Test Title')
        self.assertEqual(template.description, 'Test Description')
        self.assertEqual(template.bio, '')