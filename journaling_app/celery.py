from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Loading Celery into Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journaling_app.settings')

app = Celery('journaling_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
