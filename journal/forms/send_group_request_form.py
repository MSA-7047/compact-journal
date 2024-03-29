from django import forms
from journal.models import User, GroupRequest


class SendGroupRequestForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), label='Select User')

    class Meta:
        model = GroupRequest
        fields = ['recipient']

    def __init__(self, *args, currentUser=None, **kwargs):
        super().__init__(*args, **kwargs)
        if currentUser is not None:
            self.fields['recipient'].queryset = currentUser.friends.all()
    
    def save(self, commit=True, group=None, sender=None):
        instance = super().save(commit=False)
        if commit:
            instance.group = group
            instance.sender = sender
            instance.save()
        return instance
