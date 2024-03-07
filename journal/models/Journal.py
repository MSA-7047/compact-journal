from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Journal(models.Model):
    """Model to represent the Journals the User will be writing on."""
    journal_title = models.CharField('Title', max_length=50, blank=False)
    journal_description = models.TextField('Description', max_length=1000)
    journal_bio = CKEditor5Field('Entry', config_name='extends', max_length=10000)
    entry_date = models.DateTimeField(auto_now_add=True)
    MOOD_OPTIONS = [
        ("Sad", "Sad"),
        ("Happy", "Happy"),
        ("Angry", "Angry"),
        ("Neutral", "Neutral")
    ]
    journal_mood = models.CharField('Mood', choices=MOOD_OPTIONS, blank=False, max_length=7)
    journal_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    private = models.BooleanField(blank=False, default = False)

    class Meta:
        app_label = 'journal'
