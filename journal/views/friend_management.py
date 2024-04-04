from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from journal.models import User, FriendRequest, Notification, Points
from journal.forms import SendFriendRequestForm
from journal.views.user_management import calculate_user_points, points_to_next_level

#method to retrieve a given users pending freind requests and sent requests to be passes as context data
def get_friend_requests(user):
    requests = FriendRequest.objects.filter(recipient=user, is_accepted=False)
    pending_sent_requests = user.sent_invitations.filter(status='pending')
    rejected_sent_requests = user.sent_invitations.filter(status='rejected')
    return requests, pending_sent_requests, rejected_sent_requests


@login_required
def view_friends(request):
    friends = request.user.friends.all()
    (requests, pending_sent_requests, rejected_sent_requests) = get_friend_requests(request.user)
    form = SendFriendRequestForm()

    has_pending_requests = requests.filter(status='pending').exists()

    return render(
        request,
        template_name='friends.html',
        context={
            'form': form,
            'requests': requests,
            'sent_pending_invitations': pending_sent_requests,
            'sent_rejected_invitations': rejected_sent_requests,
            'friends':friends,
            'has_pending_requests': has_pending_requests
        })

@login_required
def view_friends_profile(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    

    totalpoints = calculate_user_points(friend)
    level_data = points_to_next_level(friend)
    points_next_level = level_data['points_to_next_level']
    points_needed = level_data['points_needed']
    recent_points = Points.objects.filter(user=friend).order_by('-id')[:5]

    return render(request, 'view_profile.html', 
                  {"user": friend, 
                   'my_profile': False, 
                   'total_points': totalpoints, 
                   'level_data': level_data,
                   'points_to_next_level': points_next_level,
                   'points_needed': points_needed,
                   'recent_points': recent_points
                   })



@login_required
def send_friend_request(request, user_id):
    if request.method == 'POST':
        form = SendFriendRequestForm(request.POST)
        if form.is_valid() and form.check_user(user=request.user):
            recipient_username = form.cleaned_data['recipient']
            recipient = User.objects.filter(username=recipient_username).all().first()
            FriendRequest.objects.get_or_create(recipient=recipient, sender=request.user, status='pending')

            notif_message = f"You have received a friend request from {request.user}."
            Notification.objects.create(notification_type="friend", message=notif_message, user=recipient)

            return redirect('send_request', user_id=user_id)
    else:
        form = SendFriendRequestForm()

    (requests, sent_pending_invitations, sent_rejected_invitations) = get_friend_requests(request.user)

    return render(
        request,
        template_name='friends.html',
        context={
            'form': form,
            'requests': requests,
            'sent_pending_invitations': sent_pending_invitations,
            'sent_rejected_invitations': sent_rejected_invitations
        }
    )


@login_required
def accept_invitation(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, recipient=request.user, is_accepted=False)

    # Add the user to the team and mark the invitation as accepted
    friend_request.recipient.friends.add(friend_request.sender)
    friend_request.sender.friends.add(friend_request.recipient)
    friend_request.is_accepted = True
    friend_request.status = 'accepted'

    sender_message = f"{friend_request.recipient} has accepted your friend request."
    receiver_message = f"You are now friends with {friend_request.sender}"
    Notification.objects.create(notification_type="friend", message=sender_message, user=friend_request.sender)
    Notification.objects.create(notification_type="friend", message=receiver_message, user=friend_request.recipient)
    Points.objects.create(user=friend_request.sender, points=30, description=f"{friend_request.recipient} has accepted your friend request.")

    friend_request.delete()


    return redirect('view_friends')


@login_required
def reject_invitation(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, recipient=request.user, is_accepted=False)
    friend_request.status = 'rejected'

    notif_message = f"Your friend request to {friend_request.recipient} has been rejected."
    Notification.objects.create(notification_type="friend", message=notif_message, user=friend_request.sender)

    friend_request.save()
    return redirect('view_friends')


@login_required
def delete_sent_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, sender=request.user)
    friend_request.delete()
    return redirect('view_friends')


@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    request.user.friends.remove(friend)

    sender_message = f"You have removed {friend} as a friend."
    receiver_message = f"{request.user} has removed you as a friend."
    Notification.objects.create(notification_type="friend", message=sender_message, user=request.user)
    Notification.objects.create(notification_type="friend", message=receiver_message, user=friend)

    friend.friends.remove(request.user)
    return redirect('view_friends')

