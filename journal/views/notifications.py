from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from journal.models import Notification


@login_required
def create_notification(request: HttpRequest, text: str, type: str) -> None:
    current_user = request.user

    Notification.objects.create(user=current_user, message=text, notification_type=type)
    messages.add_message(request, 35, text)


@login_required
def mark_notification_as_read(
    request: HttpRequest, notification_id: int
) -> HttpResponseRedirect:
    notification = get_object_or_404(
        Notification, id=notification_id, user=request.user
    )
    notification.is_read = True
    time = notification.time_created.strftime("%Y-%m-%d %H:%M:%S")
    messages.success(request, f"Notification created at {time} was marked as read.")
    notification.save()

    return redirect(notification.get_absolute_url())


@login_required
def mark_all_notification_as_read(request: HttpRequest) -> HttpResponseRedirect:
    Notification.objects.filter(user=request.user).update(is_read=True)
    messages.success(request, "All notifications cleared.")
    return redirect("dashboard")


def get_all_unread_notifications(request: HttpRequest) -> dict[str, Notification]:
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {"notifications": notifications}
    return {"notifications": []}
