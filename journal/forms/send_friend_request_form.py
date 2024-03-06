from django import forms
from journal.models import User, FriendRequest


class SendFriendRequestForm(forms.Form):

    recipient = forms.ModelChoiceField(queryset=User.objects.all(), label='Select User')

    class Meta:
        model = FriendRequest
        fields = ['recipient']

    def __init__(self, *args, user=None,  **kwargs):
        friends = user.friends.all()
        super().__init__(*args, **kwargs)
        if friends is not None:
            self.fields['recipient'].queryset = User.objects.exclude(id__in=[user.id for user in friends]).exclude(id=user.id)
