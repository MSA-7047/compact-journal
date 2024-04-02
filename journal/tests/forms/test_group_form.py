from django.test import TestCase
from journal.forms import GroupForm
from journal.models import Group

class GroupFormTestCase(TestCase):
    def setUp(self):
        self.form_data = {'name': 'Test'}

    def test_valid_form(self):
        form = GroupForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data_is_rejected(self):
        self.form_data= {}
        form = GroupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'name': ['This field is required.']})

    def test_name_of_30_char_is_accepted(self):
        self.form_data = {'name': 'x' * 30}
        form = GroupForm(self.form_data)
        self.assertTrue(form.is_valid)
    
    def test_name_of_31_char_is_rejected(self):
        self.form_data = {'name': 'x' * 31}
        form = GroupForm(self.form_data)
        self.assertFalse(form.is_valid())
    
    def test_description_of_50_char_acceoted(self):
        self.form_data = {'description': 'x' * 50}
        form = GroupForm(self.form_data)
        self.assertTrue(form.is_valid)

    def test_description_of_51_char_is_rejected(self):
        self.form_data = {'description': 'x' * 51}
        form = GroupForm(self.form_data)
        self.assertFalse(form.is_valid())

    def test_form_is_saved_correctly(self):
        form = GroupForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        
        group_instance = form.save(commit=False)
        group_instance.save()
        self.assertEqual(group_instance.name, 'Test')
        group_instance.save()

        saved_group = Group.objects.get(name='Test')
        self.assertEqual(saved_group, group_instance)