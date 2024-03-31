from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from journal.views.notifications import *
from journal.models import *
from journal.forms import *
from journal.views.user_management import calculate_user_points, points_to_next_level

def get_friend_requests_and_sent_invitations(user):
    requests = FriendRequest.objects.filter(recipient=user, is_accepted=False)
    sent_pending_invitations = user.sent_invitations.filter(status='pending')
    sent_accepted_invitations = user.sent_invitations.filter(status='accepted')
    sent_rejected_invitations = user.sent_invitations.filter(status='rejected')
    return requests, sent_pending_invitations, sent_accepted_invitations, sent_rejected_invitations


@login_required
def view_friend_requests(request):
    (requests, sent_pending_invitations,
     sent_accepted_invitations, sent_rejected_invitations) = get_friend_requests_and_sent_invitations(request.user)
    form = SendFriendRequestForm(user=request.user)

    """Notification Creation"""
    notif_message = "This is a testing notification message. It can be changed whenever I want it to."
    create_notification(request, notif_message, "info")

    return render(
        request,
        template_name='friend_requests.html',
        context={
            'form': form,
            'requests': requests,
            'sent_pending_invitations': sent_pending_invitations,
            'sent_accepted_invitations': sent_accepted_invitations,
            'sent_rejected_invitations': sent_rejected_invitations
        }
    )


@login_required
def view_friends(request):
    friends = request.user.friends.all()
    return render(request, 'friends.html', {"friends": friends})

@login_required
def view_friends_profile(request, friendID):
    friend = get_object_or_404(User, id=friendID)
    

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
        form = SendFriendRequestForm(request.POST, user=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            FriendRequest.objects.get_or_create(recipient=recipient, sender=request.user, status='pending')
            return redirect('send_request', user_id=user_id)
    else:
        form = SendFriendRequestForm(user=request.user)

    (requests, sent_pending_invitations,
     sent_accepted_invitations, sent_rejected_invitations) = get_friend_requests_and_sent_invitations(request.user)

    return render(
        request,
        template_name='friend_requests.html',
        context={
            'form': form,
            'requests': requests,
            'sent_pending_invitations': sent_pending_invitations,
            'sent_accepted_invitations': sent_accepted_invitations,
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

    friend_request.save()

    return redirect('view_friend_requests')


@login_required
def reject_invitation(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, recipient=request.user, is_accepted=False)
    friend_request.status = 'rejected'
    friend_request.save()
    return redirect('view_friend_requests')


@login_required
def delete_sent_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, sender=request.user)
    friend_request.delete()
    return redirect('view_friend_requests')


@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    request.user.friends.remove(friend)
    friend.friends.remove(request.user)
    return redirect('view_friends')

