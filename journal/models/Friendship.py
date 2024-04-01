from django.conf import settings
from django.db import models
from django.forms import ValidationError

class Friendship(models.Model):
    """Model used to facilitate friendship between 2 Users"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="main_user")
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_friend")

    class Meta:
        unique_together = ("user", "friend")

    def clean(self) -> None:
        if self.user == self.friend:
            raise ValidationError("User and Friend cannot refer to the same user")
        return super().clean()