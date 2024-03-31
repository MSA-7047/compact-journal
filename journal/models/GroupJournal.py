from django.conf import settings
from django.db import models
from journal.models import Group
from django_ckeditor_5.fields import CKEditor5Field


class GroupJournal(models.Model):
    """Model to represent the Journals the Group will be writing on."""
    journal_title = models.CharField(max_length=50, blank=False)
    journal_description = models.TextField(max_length=1000, blank=False)
    journal_bio = CKEditor5Field('Entry', config_name='extends', max_length=10000)
    entry_date = models.DateTimeField(auto_now_add=True)
    last_edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    MOOD_OPTIONS = [
        ("Sad", "Sad"),
        ("Happy", "Happy"),
        ("Angry", "Angry"),
        ("Neutral", "Neutral")
    ]
    journal_mood = models.CharField(choices=MOOD_OPTIONS, blank=False, max_length=7)
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        app_label = 'journal'
