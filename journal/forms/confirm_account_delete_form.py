from django import forms


class ConfirmDeletionForm(forms.Form):
    confirmation = forms.CharField(label='Type "YES" to confirm deletion', max_length=3)

    def clean_confirmation(self):
        confirmation = self.cleaned_data.get('confirmation')
        if confirmation != 'YES':
            raise forms.ValidationError('invalid input')
        return confirmation
