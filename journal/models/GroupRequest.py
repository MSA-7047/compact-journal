from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from journal.models import Group

class GroupRequest(models.Model):
    """"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_invitations')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_sent_invitations')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_requests', default=None)  
    creation_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    is_accepted = models.BooleanField(default=False)
    

    class Meta:
        app_label = 'journal'
        unique_together = 'recipient', 'sender'

    def clean(self):
        super().clean()
        if self.recipient == self.sender:
            raise ValidationError("The recipient and sender of the invitation can't be the same user")
        if not self.sender.groups.filter(id=self.recipient_group_id).exists():
            raise ValidationError("The sender must be the owner of the group")