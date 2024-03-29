from django import forms
from journal.models import GroupJournal

class EditGroupJournalForm(forms.ModelForm):
    """Form for editing a group journal."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["journal_bio"].required = False

    class Meta:
        model = GroupJournal
        fields = ['journal_title', 'journal_description', 'journal_bio', 'journal_mood']