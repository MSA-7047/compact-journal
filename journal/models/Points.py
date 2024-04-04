from django.conf import settings
from django.db import models
from .User import User

class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')
    points = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.user}'s points"

    class Meta:
        verbose_name_plural = "Points"
