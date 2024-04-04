from django import forms


class ConfirmDeletionForm(forms.Form):
    """Form to confirm account deletion."""

    confirmation = forms.CharField(label='Type "YES" to confirm deletion', max_length=3)

    def clean_confirmation(self):
        """Get confirmation form and ensure valid input 'YES' for form."""

        confirmation = self.cleaned_data.get('confirmation')
        if confirmation != 'YES':
            self.add_error('confirmation', 'invalid input')
            return False
        return confirmation
