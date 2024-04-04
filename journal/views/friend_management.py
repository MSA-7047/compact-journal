from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from journal.views.notifications import *
from journal.models import *
from journal.forms import *
from journal.views.user_management import calculate_user_points, points_to_next_level


def get_friend_requests_and_sent_invitations(user: User) -> tuple[FriendRequest, FriendRequest, FriendRequest, FriendRequest]:
    """Gets all the friend requests & invitations the user has recieved or sent

    Parameters
        :param user: the user who's requests & invites are needed

    Returns
        :return: A tuple of the following

            All the Friend requests the user has recieved

            All the invites the user has sent that are pending

            All the invites the user has sent that have been accepted 

            All the invites the user has sent which have been rejected"""
    
    requests = FriendRequest.objects.filter(recipient=user, is_accepted=False)
    sent_pending_invitations = user.sent_invitations.filter(status="pending")
    sent_accepted_invitations = user.sent_invitations.filter(status="accepted")
    sent_rejected_invitations = user.sent_invitations.filter(status="rejected")
    return (
        requests,
        sent_pending_invitations,
        sent_accepted_invitations,
        sent_rejected_invitations
    )


@login_required
def view_friends(request: HttpRequest) -> HttpResponse:
    """Renders the HTML Document that displays the logged-in user's friends & friend requests.
    
    Parameter:
        :param request: the HTTP request that contains some context such as who's logged in
        
    Returns:
        :return: a render containing the HTML template along with the required context"""
    friends = request.user.friends.all()
    (
        requests,
        sent_pending_invitations,
        sent_accepted_invitations,
        sent_rejected_invitations
    ) = get_friend_requests_and_sent_invitations(request.user)
    form = SendFriendRequestForm()

    has_pending_requests = requests.filter(status="pending").exists()

    return render(
        request,
        template_name="friends.html",
        context={
            "form": form,
            "requests": requests,
            "sent_pending_invitations": sent_pending_invitations,
            "sent_accepted_invitations": sent_accepted_invitations,
            "sent_rejected_invitations": sent_rejected_invitations,
            "friends": friends,
            "has_pending_requests": has_pending_requests,
        },
    )


@login_required
def view_friends_profile(request: HttpRequest, friend_id: int) -> HttpResponse:
    """Renders the HTML Document displaying the profile of another user, as a friend
    
    Paramters:
        :param request: the HTTP request that contains some context such as who's logged in
        :param friend_id: id of the user who's profile will be rendered
        
    Returns:
        :return: a render containing the HTML template along with the required context"""
    
    friend = get_object_or_404(User, id=friend_id)

    total_points = calculate_user_points(friend)
    level_data = points_to_next_level(friend)
    points_next_level = level_data["points_to_next_level"]
    points_needed = level_data["points_needed"]
    recent_points = Points.objects.filter(user=friend).order_by("-id")[:5]

    return render(
        request,
        "view_profile.html",
        {
            "user": friend,
            "my_profile": False,
            "total_points": total_points,
            "level_data": level_data,
            "points_to_next_level": points_next_level,
            "points_needed": points_needed,
            "recent_points": recent_points,
        },
    )


@login_required
def send_friend_request(request: HttpRequest, user_id: int) -> HttpResponse:
    """Sends a Friend Request to the specified user
    
    Paramters:
        :param request: the HTTP request that contains some context such as who's logged in
        :param user_id: id of the user who will get the request
        
    Returns:
        :return: a render containing the HTML template along with the required context"""
    
    if request.method == "POST":
        form = SendFriendRequestForm(request.POST)
        if form.is_valid() and form.check_user(user=request.user):
            recipient_username = form.cleaned_data["recipient"]
            recipient = User.objects.filter(username=recipient_username).all().first()
            FriendRequest.objects.get_or_create(
                recipient=recipient, sender=request.user, status="pending"
            )

            notif_message = f"You have received a friend request from {request.user}."
            Notification.objects.create(
                notification_type="friend", message=notif_message, user=recipient
            )

            return redirect("send_request", user_id=user_id)
    else:
        form = SendFriendRequestForm()

    (
        requests,
        sent_pending_invitations,
        sent_accepted_invitations,
        sent_rejected_invitations,
    ) = get_friend_requests_and_sent_invitations(request.user)

    return render(
        request,
        template_name="friends.html",
        context={
            "form": form,
            "requests": requests,
            "sent_pending_invitations": sent_pending_invitations,
            "sent_accepted_invitations": sent_accepted_invitations,
            "sent_rejected_invitations": sent_rejected_invitations,
        },
    )


@login_required
def accept_invitation(request: HttpRequest, friend_request_id: int) -> HttpResponse:
    """
    Paramters:
        :param request: the HTTP request that contains some context such as who's logged in
        :param friend_request_id: id of the user who will get the request
        
    Returns:
        :return: a redirect to the 'view_friends' url"""
    friend_request = get_object_or_404(
        FriendRequest, id=friend_request_id, recipient=request.user, is_accepted=False
    )

    # Add the user to the team and mark the invitation as accepted
    friend_request.recipient.friends.add(friend_request.sender)
    friend_request.sender.friends.add(friend_request.recipient)
    friend_request.is_accepted = True
    friend_request.status = "accepted"

    sender_message = f"{friend_request.recipient} has accepted your friend request."
    receiver_message = f"You are now friends with {friend_request.sender}"
    Notification.objects.create(
        notification_type="friend", message=sender_message, user=friend_request.sender
    )
    Notification.objects.create(
        notification_type="friend",
        message=receiver_message,
        user=friend_request.recipient,
    )
    Points.objects.create(
        user=friend_request.sender,
        points=30,
        description=f"{friend_request.recipient} has accepted your friend request.",
    )

    friend_request.delete()

    return redirect("view_friends")


@login_required
def reject_invitation(request: HttpRequest, friend_request_id: int):
    """
    Paramters:
        :param request: the HTTP request that contains some context such as who's logged in
        :param friend_request_id: id of the particular friend request
        
    Returns:
        :return: a redirect to the 'view_friends' url"""
    friend_request = get_object_or_404(
        FriendRequest, id=friend_request_id, recipient=request.user, is_accepted=False
    )
    friend_request.status = "rejected"

    notif_message = (
        f"Your friend request to {friend_request.recipient} has been rejected."
    )
    Notification.objects.create(
        notification_type="friend", message=notif_message, user=friend_request.sender
    )

    friend_request.save()
    return redirect("view_friends")


@login_required
def delete_sent_request(request: HttpRequest, friend_request_id: int) -> HttpResponseRedirect:
    """
    Paramters:
        :param request: the HTTP request that contains some context such as who's logged in
        :param friend_request_id: id of the particular friend request
        
    Returns:
        :return: a redirect to the 'view_friends' url"""
    friend_request = get_object_or_404(
        FriendRequest, id=friend_request_id, sender=request.user
    )
    friend_request.delete()
    return redirect("view_friends")


@login_required
def remove_friend(request: HttpRequest, user_id: int) -> HttpResponseRedirect:
    """Removes a user from the friend list
    
    Paramters:
        :param request: the HTTP request that contains some context such as who's logged in
        :param user_id: id of the user who will be removed
        
    Returns:
        :return: a redirect to the 'view_friends' url"""
    friend = get_object_or_404(User, id=user_id)
    request.user.friends.remove(friend)

    sender_message = f"You have removed {friend} as a friend."
    receiver_message = f"{request.user} has removed you as a friend."
    Notification.objects.create(
        notification_type="friend", message=sender_message, user=request.user
    )
    Notification.objects.create(
        notification_type="friend", message=receiver_message, user=friend
    )

    friend.friends.remove(request.user)
    return redirect("view_friends")
