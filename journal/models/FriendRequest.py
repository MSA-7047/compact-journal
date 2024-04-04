from django.conf import settings
from django.db import models


class FriendRequest(models.Model):
    """Model to organise how a User sends and recieves friend requests"""
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations')
    creation_date = models.DateField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending',blank=False, max_length=10)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Friend request from {self.sender.username} to {self.recipient.username}"
