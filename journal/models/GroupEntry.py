from django.conf import settings
from django.db import models
from journal.models import AbstractEntry, Group




class GroupEntry(AbstractEntry.AbstractEntry):
    """Model to represent the Journals the Group will be writing on."""
    last_edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        app_label = 'journal'
