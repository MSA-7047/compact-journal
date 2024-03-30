from django.core.management.base import BaseCommand, CommandError
from journal.models import (
    User,
    Group,
    GroupJournal,
    Journal,
    GroupMembership,
    Entries,
    Notification,
    Template,
    FriendRequest,
)


class Command(BaseCommand):
    """Build automation command to unseed the database."""

    help = "Seeds the database with sample data"

    def handle(self, *args, **options) -> None:
        """Unseed the database."""

        User.objects.filter(is_staff=False).delete()
        Group.objects.delete()
        GroupJournal.objects.delete()
        Journal.objects.delete()
        GroupMembership.objects.delete()
        Entries.objects.delete()
        Notification.objects.delete()
        Template.objects.delete()
        FriendRequest.objects.delete()

