from django import forms


class ConfirmAccountDeleteForm(forms.Form):
    confirmation = forms.CharField(label='Type "YES" to confirm deletion', max_length=3)

    def clean_confirmation(self):
        confirmation = self.cleaned_data.get('confirmation')
        if confirmation != 'YES':
            raise forms.ValidationError('You must type "YES" to confirm deletion.')
        return confirmation
