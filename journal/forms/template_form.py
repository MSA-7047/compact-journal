from django import forms
from journal.models import Template


class CreateTemplateForm(forms.ModelForm):
    """Form for creating a new template for Entry in Journal""".

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bio"].required = False

    class Meta:
        """"Form options."""
        model = Template
        fields = ['title', 'description', 'bio',]