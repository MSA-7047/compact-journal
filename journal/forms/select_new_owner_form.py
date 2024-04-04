from django import forms
from journal.models import User

class SelectNewOwnerForm(forms.Form):
    """Form for changing owner of a group."""
    
    new_owner = forms.ModelChoiceField(queryset=None, empty_label=None)

    def __init__(self, *args, group=None, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if group and current_user:
            # Filter the queryset based on group memberships excluding the current user
            self.fields['new_owner'].queryset = User.objects.filter(groupmembership__group=group).exclude(id=current_user.id)
