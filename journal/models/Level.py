from django.conf import settings
from django.db import models
from django.urls import reverse
from .User import User

from django.db import models
from django.conf import settings
from .Notification import Notification

class Level(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='level')
    points = models.IntegerField(default=0)
    current_level = models.IntegerField(default=1)  

    @property
    def level(self):
        return self.current_level


    def calculate_level(self, total_points=int(0)):
        level = 1
        points_needed = 100
        increment = 50
        points_to_next_level = points_needed - total_points

        while total_points >= points_needed:
            level += 1
            increment *= 1.5  
            points_needed += round(increment / 50) * 50
            points_to_next_level = points_needed - total_points
            #print("points needed for level ",level,"is",points_needed)

        return {
            'current_level': level,
            'points_to_next_level': points_to_next_level,
            'points_needed': points_needed
        }