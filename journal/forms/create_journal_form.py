from django import forms
from journal.models import Journal

class CreateJournalForm(forms.ModelForm):

    class Meta:
        model = Journal
        fields = ['title', 'summary', 'private']