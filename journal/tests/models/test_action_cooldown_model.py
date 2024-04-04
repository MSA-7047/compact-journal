from django.test import TestCase
from django.utils import timezone
from journal.models import ActionCooldown, User


class ActionCooldownTestCase(TestCase):
     """Unit tests for the Action cooldown model."""
     
    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

    def test_action_can_be_performed(self):
        past_time = timezone.now() - timezone.timedelta(hours=2)
        cooldown = ActionCooldown.objects.create(
            user=self.user,
            action_type='test_action',
            last_performed=past_time
        )

        self.assertTrue(ActionCooldown.can_perform_action(self.user, 'test_action'))

    def test_action_cannot_be_performed_within_cooldown(self):
        recent_time = timezone.now()
        cooldown = ActionCooldown.objects.create(
            user=self.user,
            action_type='test_action',
            last_performed=recent_time
        )

        self.assertFalse(ActionCooldown.can_perform_action(self.user, 'test_action'))

    def test_action_can_be_performed_if_cooldown_expired(self):
        past_time = timezone.now() - timezone.timedelta(hours=1)
        cooldown = ActionCooldown.objects.create(
            user=self.user,
            action_type='test_action',
            last_performed=past_time
        )
        self.assertTrue(ActionCooldown.can_perform_action(self.user, 'test_action'))

    def test_action_can_be_performed_if_no_previous_cooldown(self):
        self.assertTrue(ActionCooldown.can_perform_action(self.user, 'test_action'))