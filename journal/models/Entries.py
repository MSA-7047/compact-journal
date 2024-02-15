from django.db import models


class Entries(models.Model):
    a = models.CharField(max_length=1)

    class Meta:
        app_label = 'journal'
