from celery import shared_task
from django.utils import timezone
from .models import Journal, Notification, User


@shared_task
def send_journal_reminder(user_id):
    user = User.objects.get(pk=user_id)
    today = timezone.localdate()
    todays_entries = Journal.objects.filter(last_entry_date__date=today, owner=user)
    previous_entries = Journal.objects.filter(last_entry_date__date__lt=today, owner=user)

    if previous_entries.exists():
        Notification.objects.create(notification_type="reminder", message=f"{user.username}, you have one or more journals without an entry for today. Add one now!", user=user)   
    elif todays_entries.exists():
        Notification.objects.create(notification_type="reminder", message=f"Well done {user.username}! You have created an entry for all your journals today.", user=user)


@shared_task
def send_reminders_to_all_users():
    all_users = User.objects.all()
    
    for user in all_users:
        send_journal_reminder.delay(user.pk)
