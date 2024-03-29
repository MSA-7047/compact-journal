from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from journal.models import GroupRequest, Group, GroupMembership, User, GroupJournal, Notification
from journal.forms import *


@login_required
def group(request) -> HttpResponse:
    """Display the list of groups the current user is in"""
    current_user = request.user
    current_user_groups = current_user.groups.all()
    group_request = GroupRequest.objects.filter(recipient=current_user, status="Pending")
    return render(request, 'group.html', {'user': current_user, 'groups': current_user_groups, 'group_requests': group_request})


@login_required
def group_dashboard(request, group_id) -> HttpResponse:
    """Displays the journals & members of a given group"""
    current_user = request.user
    given_group = get_object_or_404(Group, pk=group_id)
    all_members_in_group = User.objects.filter(groupmembership__group=given_group)
    group_journals = GroupJournal.objects.filter(owner=given_group)
    user_membership = GroupMembership.objects.get(user=current_user, group=given_group)
    is_owner = user_membership.is_owner
    return render(
        request,
        'group_dashboard.html',
        {
            'group': given_group,
            'members': all_members_in_group,
            'journals': group_journals,
            'is_owner': is_owner
        }
    )


@login_required
def create_group(request) -> HttpResponse:
    """Display create group screen and handles create group form"""
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save(commit=True, creator=request.user)
            return redirect('groups')
    else:
        form = GroupForm()

    return render(request, 'create_group.html', {'form': form})


@login_required
def edit_group(request, group_id):
    """Allows owner of the group to edit the group."""
    group = get_object_or_404(Group, pk=group_id)
    membership = get_object_or_404(GroupMembership, group=group, user=request.user)

    form = GroupForm(instance=group)

    if not membership.is_owner:
        # User is not the owner, return forbidden response
        messages.error(request, "You are not authorized to edit this group")
        return redirect('group_dashboard', group_id=group_id)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            group.name = cleaned_data['name']
            group.save()  # Save the updated group
            messages.success(request, "Group name updated successfully.")
            return redirect('group_dashboard', group_id=group_id)

    return render(request, 'edit_group.html', {'form': form, 'group_id': group.group_id})


@login_required
def send_group_request(request, group_id):
    """Allows a user to send a group request."""
    group_ = Group.objects.get(pk=group_id)
    membership = GroupMembership.objects.filter(group=group_, user=request.user).first()

    if not membership.is_owner:
        messages.error(request, "You are not authorized to send a group request")
        return redirect('group_dashboard', group_id=group_id)

    if request.method == 'POST':
        form = SendGroupRequestForm(request.POST, currentUser=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            print(recipient)
            # Check if a request from this sender to the recipient for this group already exists
            existing_request = GroupRequest.objects.filter(sender=request.user, recipient=recipient, group=group_).first()
            if existing_request:
                messages.error(request, f"{recipient} has already been invited.")
                return render(request, 'send_group_request.html', {'form': form})

            # Create the group request
            GroupRequest.objects.create(sender=request.user, recipient=recipient, group=group_)
            Notification.objects.create(notification_type="info", message=f"{request.user} has invited you to a new group named {group_.name}.", user=recipient)

            messages.success(request, f"{recipient} has now been invited.")
            return redirect('group_dashboard', group_id=group_id)
    else:
        form = SendGroupRequestForm(currentUser=request.user)
    return render(request, 'send_group_request.html', {'form': form})

@login_required
def accept_group_request(request, group_id):
    """Allows a user that has a sent request to accept the request."""
    group = get_object_or_404(Group, group_id=group_id)
    group_request = get_object_or_404(GroupRequest, group=group, recipient=request.user)
    group_request.is_accepted = True
    group_request.status = 'accepted'

    # Create GroupMembership for the user
    GroupMembership.objects.create(user=request.user, group=group)
    Notification.objects.create(notification_type="info", message=f"{request.user} has joined your group named {group}", user=group_request.sender)

    group_request.delete()
    #invitation.delete()

    return redirect('groups')


@login_required
def reject_group_request(request, group_id):
    """Allows the user with the sent friend request to reject it"""
    group = get_object_or_404(Group, group_id=group_id)
    group_request = get_object_or_404(GroupRequest, group=group, recipient=request.user)
    group_request.status = 'rejected'

    Notification.objects.create(notification_type="info", message=f"{request.user} has rejected your group named {group}", user=group_request.sender)

    group_request.delete()
    #invitation.delete()
    return redirect('groups')


@login_required
def delete_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()

    if not membership.is_owner:
        messages.error(request, "You are not authorized to delete the group")
        return redirect('group_dashboard', {'group_id': group.group_id})

    if request.method == 'POST':
        form = ConfirmGroupDeleteForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirmation'].upper() == "YES":
            to_del = Group.objects.filter(group_id=group_id).first()
            to_del.delete()

            messages.success(request, f"The group has been deleted.")
            return redirect('dashboard')
        else:
            form.add_error('confirmation', 'Please enter "YES" to confirm deletion.')
    else:
        form = ConfirmGroupDeleteForm()

    return render(request, 'delete_group.html', {'form': form, 'group_id': group.group_id})


@login_required
def leave_group(request, group_id):
    """Allows users to leave a group"""
    group = get_object_or_404(Group, pk=group_id)
    user = request.user
    membership = get_object_or_404(GroupMembership, group=group, user=request.user)

    if membership.is_owner:
        return redirect('select_new_owner', group_id=group_id)
    else:
        membership.delete()
        return redirect('dashboard')

@login_required
def remove_player_from_group(request, group_id, player_id):
    """Allows the owner to remove a player from the group."""

    group_ = get_object_or_404(Group, pk=group_id)
    user_membership = get_object_or_404(GroupMembership, group=group_, user=request.user)
    player = get_object_or_404(User, pk=player_id)
    player_membership = get_object_or_404(GroupMembership, group=group_, user=player)

    if not user_membership.is_owner:
        return HttpResponseForbidden('You are not authorized to remove a player from this group.')

    if player_membership.is_owner:
        messages.error(request, "The owner cannot be removed from the group.")
        return redirect('group_dashboard', group_id=group_.group_id)

    try:
        membership = GroupMembership.objects.get(group=group_, user=player)
    except GroupMembership.DoesNotExist:
        messages.error(request, f"{player.username} is not a member of the group.")
        return redirect('group_dashboard', group_id=group_.group_id)

    membership.delete()
    messages.success(request, f"Successfully removed {player.username} from the group.")


    return redirect('group_dashboard', group_id=group_.group_id)

@login_required
def select_new_owner(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    membership = get_object_or_404(GroupMembership, group=group, user=request.user)

    # Ensure that the current user is the owner of the group
    if not GroupMembership.objects.filter(group=group, user=request.user, is_owner=True).exists():
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('group_dashboard', group_id=group_id)

    if request.method == 'POST':
        form = SelectNewOwnerForm(request.POST, group=group, current_user=request.user)
        if form.is_valid():
            new_owner = form.cleaned_data['new_owner']
            membership.is_owner = False
            membership.delete()
            new_owner_membership = get_object_or_404(GroupMembership, group=group, user=new_owner)
            new_owner_membership.is_owner = True
            new_owner_membership.save()
            messages.success(request, "New owner selected successfully.")
            return redirect('dashboard')
    else:
        form = SelectNewOwnerForm(group=group, current_user=request.user)

    return render(request, 'select_new_owner.html', {'form': form, 'group': group, 'user': request.user})
