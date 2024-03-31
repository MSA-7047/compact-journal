from django import forms


class ConfirmGroupDeleteForm(forms.Form):
    confirmation = forms.CharField(label='Type "YES" to confirm deletion', max_length=3)