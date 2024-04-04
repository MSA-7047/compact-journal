from django.conf import settings
from django.db import models
from .Group import Group


class GroupMembership(models.Model):
    """Model used to facilitate group memberships between users and groups"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_owner = models.BooleanField(blank=False, default=False)

    class Meta:
        app_label = 'journal'
        unique_together = 'user', 'group'
