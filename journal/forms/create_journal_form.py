from django import forms
from journal.models import Journal


class CreateJournalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["journal_bio"].required = False

    class Meta:
        model = Journal
        fields = ['journal_title', 'journal_description', 'journal_bio', 'journal_mood', 'private']
