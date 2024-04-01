from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class ActionCooldown(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cooldowns")
    action_type = models.CharField(max_length=50)
    last_performed = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'action_type')

    @staticmethod
    def can_perform_action(user, action_type, cooldown_hours=1):
        now = timezone.now()
        cooldown, created = ActionCooldown.objects.get_or_create(
            user=user, 
            action_type=action_type,
            defaults={'last_performed': now - timezone.timedelta(hours=cooldown_hours)}
        )

        if created or (now - cooldown.last_performed).total_seconds() > cooldown_hours * 3600:
            cooldown.last_performed = now
            cooldown.save()
            return True
        
        return False
