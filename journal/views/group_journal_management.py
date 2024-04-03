from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from journal.models import Group, GroupMembership, User, GroupEntry, Notification
from journal.forms import *
from django.contrib import messages


@login_required    
def create_group_journal(request, group_id):
    """View used to allow the user to create a group journal."""
    group = get_object_or_404(Group, group_id=group_id)
    membership = get_object_or_404(GroupMembership, group=group, user=request.user)

    if not membership.is_owner:
        messages.error(request, "You are not authorized to create a journal.")
        return redirect('group_dashboard', group_id=group_id)

    if request.method == 'POST':
        form = CreateGroupJournalForm(request.POST)
        if form.is_valid():
            # Save the form data to the existing GroupEntry instance
            entry = form.save(commit=False)
            entry.last_edited_by = request.user
            entry.owner = group
            entry.save()

            memberships = GroupMembership.objects.filter(group=group)
            for member in memberships:
                notif_message = f"A new group entry {entry.title} in '{group.name}' has been created."
                Notification.objects.create(notification_type="group", message=notif_message, user=member.user)

            return redirect('group_dashboard', group_id=group_id)
    else:
        form = CreateGroupJournalForm()

    return render(request, 'create_group_journal.html', {'form': form, 'group_id': group_id, 'is_edit': False})

@login_required
def edit_group_journal(request, group_id, journal_id):
    """Allows the user to edit a group journal."""
    group = get_object_or_404(Group, group_id=group_id)
    entry = get_object_or_404(GroupEntry, id=journal_id, owner=group)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()

    if request.method == 'POST':
        form = CreateGroupJournalForm(request.POST, instance=entry)
        if form.is_valid():
            # Save the form data to the existing GroupEntry instance
            entry = form.save(commit=False)
            entry.owner = group
            entry.last_edited_by = request.user

            memberships = GroupMembership.objects.filter(group=group)
            for member in memberships:
                notif_message = f"The entry {entry.title} in group '{group.name}' has been edited by {entry.last_edited_by}."
                Notification.objects.create(notification_type="group", message=notif_message, user=member.user)

            entry.save()
                    # Check the referer header to determine the previous page

            return redirect('group_dashboard', group_id=group_id)
    else:
        form = CreateGroupJournalForm(instance=entry)
    
    return render(request, 'create_group_journal.html', {'form': form, 'group_id': group_id, 'journal_id': journal_id, 'is_edit': True, 'is_owner': membership.is_owner})

@login_required
def delete_group_journal(request, group_id, journal_id):
    journal = get_object_or_404(GroupEntry, pk=journal_id)
    group = get_object_or_404(Group, group_id=group_id)
    group_membership = get_object_or_404(GroupMembership, user=request.user, group=journal.owner)
    # Allows only the owner of the group to delete the journal.
    if not group_membership.is_owner:
        messages.error(request, "You are not authorized to delete the journal.")
        return redirect('group_dashboard', group_id=group_id) 
    
    if request.method == 'POST':

        memberships = GroupMembership.objects.filter(group=group)
        for member in memberships:
            notif_message = f"The entry {journal.title} in group '{group.name}' has been deleted."
            Notification.objects.create(notification_type="group", message=notif_message, user=member.user)

        journal.delete()
        messages.success(request, f"The entry {journal.title} has been deleted successfully.")

        referer = request.META.get('HTTP_REFERER')
        if referer:
            # Check if the previous page is the group dashboard
            if 'group_dashboard' in referer:
                return redirect('group_dashboard', group_id=group_id)
            # Check if the previous page is the view group journals page
            elif 'view_group_journals' in referer:
                return redirect('view_group_journals', group_id=group_id)
            else:
                return HttpResponseRedirect(referer)
        
        return redirect('group_dashboard', group_id=group_id) 
    
    return redirect('group_dashboard', group_id=group_id) 

@login_required
def view_group_journals(request, group_id):
    """Used to allow members of a group to see all journals written by that group."""
    group = Group.objects.get(pk=group_id)
    journal_entries = GroupEntry.objects.filter(owner=group)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()

    # Initialize forms outside the condition to avoid repetition
    filter_form = EntryFilterForm(request.user, request.POST or None)
    sort_form = EntrySortForm(request.POST or None)

    if request.method == 'POST' and filter_form.is_valid() and sort_form.is_valid():
        journal_entries = filter_form.filter_entries(journal_entries)
        sort_order = sort_form.cleaned_data['sort_by_entry_date']
        journal_entries = journal_entries.order_by('-entry_date' if sort_order == 'descending' else 'entry_date')
    else:
        journal_entries = journal_entries.all()
    
    return render(request, 'group_journals.html', {'group': group, 'group_id': group_id, 'group_journals': journal_entries, 'is_owner': membership.is_owner})
