from celery import shared_task
from django.utils import timezone
from .models import Journal
from django.contrib.auth import get_user_model
from django.db.models import Count, Q

User = get_user_model()

@shared_task
def send_journal_reminder(user_id):
    user = User.objects.get(pk=user_id)
    today = timezone.localdate()
    todays_entries = Journal.objects.filter(entry_date__date=today, owner=user)
    
    if not todays_entries.exists():
        print(f"Reminder: User {user.username}, don't forget to complete your journal for today!")
    else:
        print(f"User {user.username} has already made a journal entry for today.")

@shared_task
def send_reminders_to_all_users():
    today = timezone.localdate()
    users = User.objects.annotate(
        todays_entries_count=Count('journals', filter=Q(journals__entry_date__date=today))
    ).filter(todays_entries_count=0)
    
    for user in users:
        send_journal_reminder.delay(user.pk)


