from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from journal.models import GroupRequest, Group, GroupMembership, User
from journal.forms import *


@login_required
def group(request) -> HttpResponse:
    """Display the list of groups the current user is in"""
    current_user = request.user
    current_user_groups = current_user.groups.all()
    return render(request, 'group.html', {'user': current_user, 'groups': current_user_groups})


@login_required
def group_dashboard(request, given_group_id) -> HttpResponse:
    """Displays the journals & members of a given group"""
    current_user = request.user
    given_group = get_object_or_404(Group, pk=given_group_id)
    all_members_in_group = ...
    group_journals = ...
    is_owner = ...
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
def group(request) -> HttpResponse:
    """Display the list of groups the current user is in"""
    current_user = request.user
    current_user_groups = current_user.groups
    return render(request, 'group.html', {'user': current_user, 'groups': current_user_groups})


@login_required
def edit_group(request, group_id):
    """Allows owner of the group to edit the group."""
    group = get_object_or_404(Group, pk=group_id)

    if request.user != group.owner:
        # User is not the owner, return forbidden response
        return HttpResponseForbidden('You are not authorized to edit this group')

    if request.method != 'POST':
        form = GroupForm(instance=group)
        return render(request, 'edit_group.html', {'form': form})

    form = GroupForm(request.POST, instance=group)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'Group edited successfully'})

    return JsonResponse({'errors': form.errors}, status=400)


@login_required
def send_group_request(request):
    """Allows a user to send a group request."""
    if request.method == 'POST':
        form = SendGroupRequestForm(request.POST, currentUser=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            GroupRequest.objects.create(sender=request.user, recipient=recipient)
            return redirect('home')
    else:
        form = SendGroupRequestForm(currentUser=request.user)
    return render(request, 'send_group_request.html', {'form': form})


@login_required
def accept_group_request(request, group_request_id):
    """Allows a user that has a sent request to accept the request."""
    group_request = get_object_or_404(GroupRequest, id=group_request_id, recipient=request.user, is_accepted=True)

    # Add the user to the group
    group_ = group_request.group  # Assuming group_request has a ForeignKey to Group model
    user = group_request.sender  # The user who sent the group request

    # Create GroupMembership for the user
    GroupMembership.objects.create(user=user, group=group_)

    group_request.status = 'accepted'
    group_request.save()
    #invitation.delete()

    return redirect('group')


@login_required
def reject_group_invitation(request, group_request_id):
    """Allows the user with the sent friend request to reject it"""
    group_request = get_object_or_404(GroupRequest, id=group_request_id, recipient=request.user, is_accepted=False)
    group_request.status = 'rejected'
    group_request.save()
    #invitation.delete()
    return redirect('group')


@login_required
def delete_group(request, group_id):
    """Allows the owner to delete the group"""
    group = get_object_or_404(Group, pk=group_id)

    if request.user == group.owner:
        # Only allow deletion via POST method to prevent accidental deletions
        if request.method == 'POST':
            group.delete()
            return redirect('home')
        else:
            # Handle GET requests (e.g., show a confirmation page)
            return render(request, 'confirm_group_deletion.html', {'group': group})
    else:
        return HttpResponseForbidden('You are not authorized to delete this group.')


@login_required
def leave_group(request, group_id):
    """Allows users to leave a group"""
    group = get_object_or_404(Group, pk=group_id)
    user = request.user

    if user != group.owner:
        group_membership = GroupMembership.objects.get(group=group, user=user)
        group_membership.delete()

        if group.members.count() == 0:
            group.delete()

        return redirect('home')

    if group.members.count() == 1:
        # The owner is the only member, delete the group
        group.delete()
        return redirect('home')

    # The owner must select a new owner before leaving
    if request.method == 'POST':
        new_owner_id = request.POST.get('new_owner')
        new_owner = get_object_or_404(User, pk=new_owner_id)
        group.owner = new_owner
        group.save()

    return render(request, 'select_new_owner.html', {'group': group})


@login_required
def remove_player_from_group(request, group_id, player_id):
    """Allows the owner to remove a player from the group."""

    group_ = get_object_or_404(Group, id=group_id)
    player = get_object_or_404(User, id=player_id)

    if request.user != group_.owner:
        return HttpResponseForbidden('You are not authorized to remove a player from this group.')

    if player == group_.owner:
        messages.error(request, "The owner cannot be removed from the group.")
        return redirect('group_detail', group_id=group.id)

    try:
        membership = GroupMembership.objects.get(group=group_, user=player)
    except GroupMembership.DoesNotExist:
        messages.error(request, f"{player.username} is not a member of the group.")
        return redirect('group_detail', group_id=group_.id)

    membership.delete()
    messages.success(request, f"Successfully removed {player.username} from the group.")

    if group_.members.count() == 0:
        group_.delete()
        messages.info(request, "The group has been deleted as there are no members left.")

    return redirect('group_detail', group_id=group_.id)

