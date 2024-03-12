from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from .User import User


class Template(models.Model):
    """Model to represent the Journals the User will be writing on."""
    title = models.CharField('Title', max_length=50, blank=False)
    description = models.TextField('Description', max_length=1000)
    bio = CKEditor5Field('Entry', config_name='extends', max_length=10000)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        app_label = 'journal'