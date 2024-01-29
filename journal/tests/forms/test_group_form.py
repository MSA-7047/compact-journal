from django.test import TestCase
from journal.forms import GroupForm
from journal.models import Group

class GroupFormTestCase(TestCase):
    def setUp(self):
        self.form_data = {'name': 'Test'}

    def test_valid_form(self):
        form = GroupForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        self.form_data= {}
        form = GroupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'name': ['This field is required.']})

    def test_save_method(self):
        form = GroupForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        
        group_instance = form.save(commit=False)
        group_instance.save()
        self.assertEqual(group_instance.name, 'Test')
        group_instance.save()
        
        saved_group = Group.objects.get(name='Test')
        self.assertEqual(saved_group, group_instance)