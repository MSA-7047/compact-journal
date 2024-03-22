from django.db import models
from django.conf import settings

class Journal(models.Model):
    title = models.CharField('Title', max_length=50, blank=False)
    summary = models.TextField('Description', max_length=1000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        app_label = 'journal'
