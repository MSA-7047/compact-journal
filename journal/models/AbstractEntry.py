from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django_ckeditor_5.fields import CKEditor5Field


class AbstractEntry(models.Model):
    """Model to represent the Entries the User will be writing in."""
    
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
        ("Surprised", "Surprised"),
        ("Hopeful", "Hopeful"),
        ("Frustrated", "Frustrated"),
        ("Grateful", "Grateful"),
        ("Relaxed", "Relaxed"),
        ("Optimistic", "Optimistic"),
        ("Anxious", "Anxious"),
    ]
    mood = models.CharField('Mood', choices=MOOD_OPTIONS, blank=False, max_length=20)

    class Meta:
        abstract = True

    #Form validator to check for correctness
    def clean(self) -> None:

        if len(self.content) > 10_000:
            raise ValidationError("Content has exceeded allowable limit of 10,000")
        if len(self.summary) > 200:
            raise ValidationError("Summary must be less than 200 characters")
        return super().clean()

