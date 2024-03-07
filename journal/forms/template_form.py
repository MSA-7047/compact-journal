"""Forms for the journal app."""
from django import forms
from journal.models import Template


class CreateTemplateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bio"].required = False

    class Meta:
        model = Template
        fields = ['title', 'description', 'bio',]