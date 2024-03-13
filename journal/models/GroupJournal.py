from django.conf import settings
from django.db import models
from journal.models import Group


class GroupJournal(models.Model):
    """Model to represent the Journals the Group will be writing on."""
    journal_title = models.CharField(max_length=50, blank=False)
    journal_description = models.TextField(max_length=1_000)
    journal_bio = models.TextField(max_length=10_000)
    entry_date = models.DateTimeField(auto_now_add=True)
    MOOD_OPTIONS = [
        ("Sad", "Sad"),
        ("Happy", "Happy"),
        ("Angry", "Angry"),
        ("Neutral", "Neutral")
    ]
    journal_mood = models.CharField(choices=MOOD_OPTIONS, blank=False, max_length=7)
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)
    private = models.BooleanField(blank=False)

    class Meta:
        app_label = 'journal'
