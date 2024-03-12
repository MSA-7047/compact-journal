from django import forms
from journal.models import User


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'dob',
            'bio',
            'location',
            'nationality'
        ]

        labels = {
            'dob': 'Date of Birth',
            'nationality': 'Nationality'
        }

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
