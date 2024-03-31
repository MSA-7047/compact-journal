from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Sum
from .models import Level, Points
from .views.notifications import Notification
from django.contrib import messages
from .models.Notification import UserMessage

User = get_user_model()

# Signal to create/update Level when a new user is created
@receiver(post_save, sender=User)
def create_or_update_user_level(sender, instance, created, **kwargs):
    Level.objects.get_or_create(user=instance)  # Create a new Level object if it doesn't exist


# Signal to update Level when Points are added/updated
@receiver(post_save, sender=Points)
def update_level_on_points_change(sender, instance, created, **kwargs):
    if created:
        user_level, _ = Level.objects.get_or_create(user=instance.user)
        total_points = Points.objects.filter(user=instance.user).aggregate(Sum('points'))['points__sum'] or 0
        print("Total points in the signals is read as:", total_points)
        calculated_level = user_level.calculate_level(total_points)['current_level']

        if calculated_level > user_level.current_level:
            Notification.objects.create(
                user=instance.user,
                message=f"Congratulations, you have levelled up to level {calculated_level}!",
                notification_type = "points"
            )
            UserMessage.objects.create(user=instance.user, message=f"Congratulations, you have leveled up to level {calculated_level}!")
            
        user_level.current_level = calculated_level  # Update this line to use the correct field
        user_level.save()
