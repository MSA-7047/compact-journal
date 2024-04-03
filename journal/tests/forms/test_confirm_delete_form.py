from django.test import TestCase
from journal.forms import ConfirmDeletionForm

class ConfirmAccountDeleteFormTest(TestCase):
    def test_confirm_deletion_with_valid_input(self):
        form_data = {'confirmation': 'YES'}
        form = ConfirmDeletionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_confirm_deletion_with_invalid_input(self):
        invalid_form_data = {'confirmation': 'NO'}
        form = ConfirmDeletionForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())

    def test_confirm_deletion_with_empty_input(self):
        empty_form_data = {'confirmation': ''}
        form = ConfirmDeletionForm(data=empty_form_data)
        self.assertFalse(form.is_valid())

    def test_confirm_deletion_with_wrong_length_input(self):
        invalid_length_form_data = {'confirmation': 'YESSS'}
        form = ConfirmDeletionForm(data=invalid_length_form_data)
        self.assertFalse(form.is_valid())
