
from django import forms
from journal.models import User, FriendRequest

class SendFriendRequestForm(forms.Form):
    """"""

    recipient = forms.CharField(label='Select User')

    class Meta:
        model = FriendRequest
        fields = ['recipient']

    def check_user(self, user=None):
        """"""
        recipient = self.cleaned_data.get('recipient')
        if user:
            for friend in user.friends.all():
                if friend.username == recipient:
                    self.add_error("recipient", "User is already your friend")
                    return False

            if recipient == user.username:
                self.add_error("recipient", "Cannot request yourself")
                return False

            if not User.objects.filter(username=recipient).exists():
                self.add_error("recipient", "This user doesnt exists")
                return False

            return True
