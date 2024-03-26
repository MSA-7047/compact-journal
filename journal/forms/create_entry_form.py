from django import forms
from journal.models import Entry


class CreateEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["content"].required = False

    class Meta:
        model = Entry
        fields = ['title', 'summary', 'content', 'mood', 'private']
