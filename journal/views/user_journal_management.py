from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist
from journal.models import *
from journal.forms import *
from django.contrib import messages

@login_required
def create_journal(request):

    form = CreateJournalForm()
    if request.method != 'POST':
        return render(request, 'create_journal.html', {'form': form})

    form = CreateJournalForm(request.POST)
    if not form.is_valid():
        print("inbalid form")
        return render(request, 'create_journal.html', {'form': form})

    journal = Journal.objects.create(
        title=form.cleaned_data.get("title"),
        summary=form.cleaned_data.get("summary"),
        owner=request.user
    )
    journal.save()
    print("success")

    return redirect('/dashboard/')

@login_required
def edit_journal(request, journal_id): 
    current_user = request.user
    try:
        journal = Journal.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        messages.warning(request, "premmision denied")
        return redirect('dashboard')
    
    if journal.owner != current_user:
        messages.warning(request, "premmision denied")

    if request.method == 'POST':
        form = CreateJournalForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = CreateJournalForm(instance=journal)

    return render(request, 'create_journal.html', {'form': form, 'journal': journal, 'title': "Update Journal"})


@login_required
def delete_journal(request, journal_id):
    current_user = request.user
    try:
        journal = Journal.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        return render(request, 'permission_denied.html', {'reason': "Journal doesn not exists"})
    
    if journal.owner != current_user:
        return render(request, 'permission_denied.html')
    journal.delete()
    return redirect('dashboard')

@login_required
def journal_dashboard(request, journal_id):
    current_user = request.user
    today = datetime.now().date()

    try:
        journalobject = Journal.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        return render(request, 'permission_denied.html', {'reason': "Journal doesn not exists"})
    
    if journalobject.owner != current_user:
        return render(request, 'permission_denied.html')
    
    journal_entries = Entry.objects.filter(journal = journalobject)
    print(journal_entries)
    todays_entry = journal_entries.filter(entry_date__date = today)
    print(todays_entry)
    return render(request, 'journal_dashboard.html', {'user': current_user,'journal': journalobject, 'journal_entries': journal_entries, "todays_entry": todays_entry})

def view_entry(request, entry_id):

    current_user = request.user

    try:
        entry = Entry.objects.get(id=entry_id)
    except ObjectDoesNotExist:
        return render(request, 'permission_denied.html',)
    
    if entry.owner != current_user:
        return render(request, 'permission_denied.html', {'reason': "You do not own this journal"} )
    
    return render(request, 'entry_detail.html', {'user': current_user, 'entry': entry})


@login_required
def create_entry(request, journal_id):
    today = datetime.now().date()
    current_user = request.user

    try:
        journal = Entry.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        return render(request, 'permission_denied.html',)
    
    if journal.owner != current_user:
        return render(request, 'permission_denied.html', {'reason': "You do not own this journal"} )

    
    if Entry.objects.filter(journal = journal).filter(entry_date__date = today):
        return render(request, 'permission_denied.html', {'reason': "Daily journal already created"} )

    form = CreateEntryForm()
    if request.method != 'POST':
        return render(request, 'create_entry.html', {'form': form})

    form = CreateEntryForm(request.POST)
    if not form.is_valid():
        return render(request, 'create_entry.html', {'form': form})

    entry = Entry.objects.create(
        title=form.cleaned_data.get("title"),
        summary=form.cleaned_data.get("summary"),
        content=form.cleaned_data.get("content"),
        mood=form.cleaned_data.get("mood"),
        owner=request.user,
        journal = journal
    )
    entry.save()

    return redirect('/dashboard/')

@login_required
def edit_entry(request, entry_id): 
    current_user = request.user
    try:
        entry = Entry.objects.get(id=entry_id)
    except ObjectDoesNotExist:
        messages.warning(request, "premmision denied")
        return redirect('dashboard')

    
    if entry.owner != current_user:
        messages.warning(request, "premmision denied")

    if request.method == 'POST':
        form = CreateEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the detail view of the edited journal
    else:
        form = CreateEntryForm(instance=entry)

    return render(request, 'create_entry.html', {'form': form, 'entry': entry, 'title': "Update entry"})


@login_required
def delete_entry(request, entry_id):
    current_user = request.user
    try:
        entry = Entry.objects.get(id=entry_id)
    except ObjectDoesNotExist:
        return render(request, 'permission_denied.html', {'reason': "Journal doesn not exists"})
    
    if entry.owner != current_user:
        return render(request, 'permission_denied.html')
    entry.delete()
    return redirect('dashboard')



@login_required
def my_journals_view(request, userID):
    current_user = get_object_or_404(User, id = userID)
    isLoggedInUser = current_user == request.user
    if request.method == 'POST':
        filter_form = JournalFilterForm(current_user, request.POST)

        if filter_form.is_valid():
            myJournals = filter_form.filter_tasks()
            myJournals = myJournals.filter(journal_owner=current_user)
            sort_form = JournalSortForm(request.POST) 
            if sort_form.is_valid():
                sort_order = sort_form.cleaned_data['sort_by_entry_date']
                if sort_order == 'descending':
                    myJournals = myJournals.order_by("entry_date")
                    myJournals = myJournals.reverse()
                elif sort_order == 'ascending':
                    myJournals = myJournals.order_by("entry_date")    
        else:
            sort_form = JournalSortForm()
            myJournals = Entry.objects.filter(journal_owner=current_user)
            if not isLoggedInUser:
                myJournals = myJournals.filter(private=False)
            context = {
            'filter_form': filter_form,
            'sort_form': sort_form,
            'show_alert':True,
            'myJournals': myJournals,
            'journal_param': my_journals_to_journal_param(myJournals),
            'user': current_user,
            'isUserCurrentlyLoggedIn': isLoggedInUser
            }
            return render(request, 'My_Journals.html', context)
        
        if not isLoggedInUser:
            myJournals = myJournals.filter(private=False)

        context = {
            'filter_form': filter_form,
            'sort_form': sort_form,
            'myJournals': myJournals,
            'journal_param': my_journals_to_journal_param(myJournals),
            'user': current_user,
            'isUserCurrentlyLoggedIn': isLoggedInUser
        }
        return render(request, 'my_journals.html', context) 
    
    myJournals = Entry.objects.filter(owner=current_user)

    if not isLoggedInUser:
            myJournals = myJournals.filter(private=False)

    filter_form = JournalFilterForm(current_user)
    sort_form = JournalSortForm()
    
    context = {
            'filter_form': filter_form,
            'sort_form': sort_form,
            'myJournals': myJournals or False,
            'user': current_user,
            'journal_param': my_journals_to_journal_param(myJournals),
            'isUserCurrentlyLoggedIn': isLoggedInUser
        }
    
    return render(request, 'my_journals.html', context)   


def my_journals_to_journal_param(myJournals):
    journals = []
    for journal in myJournals:
        journals.append(f"{journal.id}")
    journal_param = ','.join(journals)
    return journal_param