from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from journal.models import GroupRequest, Group, GroupMembership, User, GroupJournal
from journal.forms import *


@login_required    
def create_group_journal(request, group_id):
    """View used to allow the user to create a group journal."""
    group_ = get_object_or_404(Group, group_id=group_id)
    membership = get_object_or_404(GroupMembership, group=group_, user=request.user)

    if not membership.is_owner:
        messages.error(request, "You are not authorized to create a journal.")
        return redirect('group_dashboard', group_id=group_id)

    form = CreateGroupJournalForm()
    if request.method == 'POST':
        form = CreateGroupJournalForm(request.POST)
        if not form.is_valid():
            return render(request, 'create_group_journal.html', {'form': form, 'group_id': group_id})
    
        journal = GroupJournal.objects.create(
            journal_title = form.cleaned_data.get('journal_title'),
            journal_description = form.cleaned_data.get('journal_description'),
            journal_bio = form.cleaned_data.get('journal_bio'),
            journal_mood = form.cleaned_data.get('journal_mood'),
            owner = group_,
            last_edited_by = request.user
        )
        journal.save()
        return redirect('group_dashboard', group_id=group_id)

    return render(request, 'create_group_journal.html', {'form': form, 'group_id': group_id})

@login_required
def edit_group_journal(request, group_id, journal_id): 
    """Allows the user to edit a group journal."""
    group_ = get_object_or_404(Group, group_id=group_id)
    journal = get_object_or_404(GroupJournal, id=journal_id, owner=group_)
    form = EditGroupJournalForm(instance=journal)
    if request.method == 'POST':
        form = EditGroupJournalForm(request.POST, instance=journal)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Update the GroupJournal instance with the new data
            journal.journal_title = cleaned_data['journal_title']
            journal.journal_description = cleaned_data['journal_description']
            journal.journal_bio = cleaned_data['journal_bio']
            journal.journal_mood = cleaned_data['journal_mood']
            journal.last_edited_by = request.user
            journal.save()

            return redirect('group_dashboard', group_id=group_id)
    return render(request, 'create_group_journal.html', {'form': form, 'group_id': group_id}) 

@login_required
def delete_group_journal(request, group_id, journal_id):
    """Allows the owner to delete a group journal."""
    journal = get_object_or_404(GroupJournal, pk=journal_id)
    group_membership = get_object_or_404(GroupMembership, user=request.user, group=journal.owner)
    # Allows only the owner of the group to delete the journal.
    if not group_membership.is_owner:
        messages.error(request, "You are not authorized to delete the journal.")
        return redirect('group_dashboard', group_id=group_id) 
    
    if request.method == 'POST':
        journal.delete()
        messages.success(request, "Journal has been deleted successfully")
        return redirect('group_dashboard', group_id=group_id) 
    
    return redirect('group_dashboard', group_id=group_id) 

@login_required
def view_group_journals(request, group_id):
    """Used to allow members of a group to see all journals written by that group."""
    group = Group.objects.get(pk=group_id)
    group_journals = GroupJournal.objects.filter(owner=group)
    return render(request, 'group_journals.html', {'group_id': group_id, 'group_journals': group_journals})