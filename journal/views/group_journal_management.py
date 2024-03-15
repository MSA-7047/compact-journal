from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from journal.models import GroupRequest, Group, GroupMembership, User, GroupJournal
from journal.forms import *


@login_required    
def create_group_journal(request):
    """View used to allow the user to create a group journal."""

    form = CreateGroupJournalForm()
    if request.method == 'POST':
        return render('request', template_name= 'add_group_journal.html', context= {'form': form})
    
    form = CreateGroupJournalForm(request.POST)
    if not form.is_valid():
        return render('request', template_name= 'add_group_journal.html', context= {'form': form})
    
    journal = GroupJournal.objects.create(
        journal_title = form.cleaned_data.get('journal_title'),
        journal_description = form.cleaned_data.get('journal_description'),
        journal_bio = form.cleaned_data.get('journal_bio'),
        journal_mood = form.cleaned_data.get('journal_mood'),
        is_private = form.cleaned_data.get('is_private'),
        journal_group = request.group,
    )
    journal.save()

    return redirect('dashboard')

@login_required
def edit_group_journal(request, journalID): 
    """Allows the user to edit a group journal."""
    journal = get_object_or_404(Journal, id=journalID)
    if request.method == 'POST':
        form = EditGroupJournalForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EditGroupJournalForm(instance=journal)

@login_required
def delete_group_journal(request, journal_id):
    """Allows the owner to delete a group journal."""
    journal = get_object_or_404(GroupJournal, pk=journal_id)
    group_membership = GroupMembership.objects.filter(user=request.user, group=journal.journal_group).first()

    # Allows only the owner of the group to delete the journal.
    if not group_membership or not group_membership.is_owner:
        return redirect('dashboard') 
    if request.method == 'POST':
        journal.delete()
        return redirect('dashboard') 
    return render(request, 'dashboard')

@login_required
def view_all_group_journals(request, group_id):
    """Used to allow members of a group to see all journals written by that group."""
    group = get_object_or_404(Group, pk=group_id)
    group_journals = GroupJournal.objects.filter(journal_group=group)
    return render(request, 'group_journals.html', {'group': group, 'group_journals': group_journals})