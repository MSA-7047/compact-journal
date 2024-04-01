from django.conf import settings
from django.db import models
from journal.models import Journal, AbstractEntry


class Entry(AbstractEntry.AbstractEntry):
    """Model to represent the Journals the User will be writing on."""
    last_edited = models.TimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entries')
    private = models.BooleanField(blank=False, default = False)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='entries')

    class Meta:
        app_label = 'journal'
