from django import forms
from journal.models import User, GroupRequest


class SendGroupRequestForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=User.objects.none(), label='Select User')

    class Meta:
        model = GroupRequest
        fields = ['recipient']

    def __init__(self, *args, currentUser=None, **kwargs):
        super().__init__(*args, **kwargs)
        if currentUser is not None:
            self.fields['recipient'].queryset = currentUser.friends.all()
