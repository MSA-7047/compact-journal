from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from journal.models import Notification

@login_required
def create_notification(request):
    current_user = request.user

    Notification.objects.create(
        user=current_user,
        message="This is a test notification message."
    )

    print("I am testing the notifications system, object creation. If this message shows, it works :)")
    messages.success(request, "Notification created!")
    
@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    if notification.is_read:
        notification.is_read = False
    else:
        notification.is_read = True
    time = notification.timeCreated.strftime("%Y-%m-%d %H:%M:%S")
    messages.success(request, f"Notification for the {notification.notification_type} created at {time} was marked as read.")
    notification.save()

    return redirect(notification.get_absolute_url())


@login_required
def mark_all_notification_as_read(request):
    Notification.objects.filter(user=request.user).update(is_read=True)
    messages.success(request, "All notifications cleared.")
    return redirect('dashboard')

def notification_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {'notifications': notifications}
    else:
        return {'notifications': []}
    
# @login_required
# def notifications_panel(request):
#     # Fetch notifications for the current user
#     notifications = Notification.objects.filter(user=request.user)
