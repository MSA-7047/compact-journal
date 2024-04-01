from django.core.management.base import BaseCommand, CommandError
from time import sleep
from journal.models import (
    ActionCooldown,
    Entry,
    FriendRequest,
    Friendship,
    Group,
    GroupEntry,
    GroupMembership,
    GroupRequest,
    Journal,
    Level,
    Notification,
    Points,
    Template,
    User
)


class Command(BaseCommand):
    """Build automation command to unseed the database."""

    help = "Seeds the database with sample data"

    def handle(self, *args, **options) -> None:
        """Unseed the database."""

        User.objects.filter(is_staff=False).delete()
        ActionCooldown.objects.all().delete()
        Friendship.objects.all().delete()
        GroupEntry.objects.all().delete()
        GroupRequest.objects.all().delete()
        Level.objects.all().delete()
        Points.objects.all().delete()
        Group.objects.all().delete()
        Journal.objects.all().delete()
        GroupMembership.objects.all().delete()
        Entry.objects.all().delete()
        Notification.objects.all().delete()
        Template.objects.all().delete()
        FriendRequest.objects.all().delete()

        print("Database unseeded")

