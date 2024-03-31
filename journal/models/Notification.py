from django.conf import settings
from django.db import models
from django.urls import reverse
from .User import User

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('reminder', 'Reminder'),
        ('points', 'Points'),
    ]

    notification_type = models.CharField(max_length=15, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        """ Returns the URL to which the notification should redirect """
        return reverse('dashboard')  # Redirecting to the dashboard by default

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"
    
    class Meta:
        ordering = ['-time_created']
    

class UserMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)