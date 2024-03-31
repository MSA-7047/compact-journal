from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from .Journal import Journal


class Entry(models.Model):
    """Model to represent the Journals the User will be writing on."""
    title = models.CharField('Title', max_length=30, blank=False)
    summary = models.TextField('Summary', max_length=200)
    content = CKEditor5Field('Entry Content', config_name='extends', max_length=10000)
    entry_date = models.DateTimeField(auto_now_add=True)
    last_edited = models.TimeField(auto_now=True)
    MOOD_OPTIONS = [
        ("Sad", "Sad"),
        ("Happy", "Happy"),
        ("Angry", "Angry"),
        ("Neutral", "Neutral"),
        ("Excited", "Excited"),
        ("Confused", "Confused"),
        ("Content", "Content"),
        ("Surprised", "Surprised"),
        ("Calm", "Calm"),
        ("Hopeful", "Hopeful"),
        ("Frustrated", "Frustrated"),
        ("Grateful", "Grateful"),
        ("Inspired", "Inspired"),
        ("Relaxed", "Relaxed"),
        ("Optimistic", "Optimistic"),
        ("Proud", "Proud"),
        ("Anxious", "Anxious"),
        ("Enthusiastic", "Enthusiastic"),
    ]
    mood = models.CharField('Mood', choices=MOOD_OPTIONS, blank=False, max_length=20)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entries')
    private = models.BooleanField(blank=False, default = False)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='entries')

    class Meta:
        app_label = 'journal'
