from django.db import models
from django.conf import settings

class Journal(models.Model):
    """Model to create a given Journal, after which they can add Entries"""
    title = models.CharField('Title', max_length=30, blank=False)
    summary = models.TextField('Description', max_length=500)
    entry_date = models.DateTimeField(auto_now_add=True)
    last_entry_date = models.DateTimeField(auto_now_add=False, null=True)
    private = models.BooleanField(blank=False, default = False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journals')

    class Meta:
        app_label = 'journal'
