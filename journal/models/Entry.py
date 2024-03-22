from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from .Journal import Journal


class Entry(models.Model):
    """Model to represent the Journals the User will be writing on."""
    title = models.CharField('Title', max_length=50, blank=False)
    summary = models.TextField('Description', max_length=1000)
    content = CKEditor5Field('Entry', config_name='extends', max_length=10000)
    entry_date = models.DateTimeField(auto_now_add=True)
    last_edited = models.TimeField(auto_now=True)
    MOOD_OPTIONS = [
        ("Happy", "Happy"),
        ("Angry", "Angry"),
        ("Neutral", "Neutral")
    ]
    mood = models.CharField('Mood', choices=MOOD_OPTIONS, blank=False, max_length=7)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    private = models.BooleanField(blank=False, default = False)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    class Meta:
        app_label = 'journal'
