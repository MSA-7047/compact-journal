from django import forms
from journal.models import User, FriendRequest

class SendFriendRequestForm(forms.Form):
    """Form for sendning a friend request."""

    recipient = forms.CharField(label='Select User')

    class Meta:
        """Form options."""

        model = FriendRequest
        fields = ['recipient']

    def check_user(self, user=None):
        """Check if recipient of request is a valid user."""
        
        recipient = self.cleaned_data.get('recipient')
        if user:
            for friend in user.friends.all():
                if friend.username == recipient:
                    self.add_error("recipient", "User is already your friend")
                    return False

            if recipient == user.username:
                self.add_error("recipient", "Cannot request yourself")
                return False

            elif not User.objects.filter(username=recipient).exists():
                self.add_error("recipient", "This user doesn't exist")
                return False

            else: 
                return True
