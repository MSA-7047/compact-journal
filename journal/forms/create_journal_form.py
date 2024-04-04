from django import forms
from journal.models import Journal

class CreateJournalForm(forms.ModelForm):
    """Form for creating a User/Personal Journal."""

    class Meta:
        """Form Options."""
        
        model = Journal
        fields = ['title', 'summary', 'private']