from AbstractJournal import AbstractJournal
from Group import Group
from django.db import models


class GroupJournal(AbstractJournal):
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        app_label = 'journal'
