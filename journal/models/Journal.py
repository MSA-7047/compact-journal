from django.db import models
from django.conf import settings

class Journal(models.Model):
    title = models.CharField('Title', max_length=30, blank=False)
    summary = models.TextField('Description', max_length=500)
    entry_date = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(blank=False, default = False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journals')

    class Meta:
        app_label = 'journal'
