from django import forms
from journal.models import GroupEntry

class CreateGroupJournalForm(forms.ModelForm):
    """Form for creating a group journal."""

    def __init__(self, *args, **kwargs):
        """Construct new group form instance with content set to false."""
        
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        """Form options."""

        model = GroupEntry
        fields = ['title', 'summary', 'content', 'mood']
