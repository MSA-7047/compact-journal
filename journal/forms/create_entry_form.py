from django import forms
from journal.models import Entry


class CreateEntryForm(forms.ModelForm):
    """Form to create Entry in a Journal"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        """Form options."""

        model = Entry
        fields = ['title', 'summary', 'content', 'mood', 'private']
