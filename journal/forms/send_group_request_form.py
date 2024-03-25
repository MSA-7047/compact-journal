from django import forms
from journal.models import User


class SendGroupRequestForm(forms.Form):

    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        label='Select User'
    )

    def __init__(self, *args, currentUser=None, **kwargs):
        super().__init__(*args, **kwargs)
        if currentUser is not None:
            self.fields['recipient'].queryset = User.objects.exclude(
                username=currentUser.username
            )
