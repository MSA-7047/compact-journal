from django import forms


class ConfirmAccountDeleteForm(forms.Form):
    confirmation = forms.CharField(label='Type "YES" to confirm deletion', max_length=3)
