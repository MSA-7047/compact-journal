
from django import forms
from journal.models import User, FriendRequest

class SendFriendRequestForm(forms.Form):

    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Select User'
    )

    class Meta:
        model = FriendRequest
        fields = ['recipient']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['recipient'].queryset = User.objects.exclude(id=user.id)
            friends = user.friends.all()
            if friends.exists():
                self.fields['recipient'].queryset = User.objects.exclude(
                    id__in=[friend.id for friend in friends]).exclude(id=user.id)
