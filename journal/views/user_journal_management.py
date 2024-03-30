from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist
from journal.models import *
from journal.forms import *
from django.contrib import messages
from journal.views.notifications import *
from journal.views.user_management import *

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

    journal_title = form.cleaned_data.get("title")

    """Notification & Points Creation"""
    notif_message = f"New journal {journal_title} created!"
    create_notification(request, notif_message, "info")
    give_points(request, 50, f"New journal {journal_title} created.")

    return redirect('/dashboard/')

def create_first_journal(current_user):
    Journal.objects.create(
        title="Welcome To Compact Journals",
        summary="""This is your first Compact Journal.
         With each compact journal you can create a daily entry to keep track of ur activites and productivity as well as ur mood
         You can create as many journals as you want to keep track of all the different aspects of your life
         Journals can be edited from the journal dashboard (press view button to access) as well as deleted
         The journal dashboard is where youy can create your daily entry and keep track of all your previous ones
        """,
        owner=current_user
    )

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

    return render(request, 'create_journal.html', {'form': form, 'journal': journal, 'title': "Update Journal", "update": True})


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
def all_journals_view(request, user_id):
    current_user = request.user
    viewing_user = User.objects.get(id=user_id)
    currently_logged_in = current_user == viewing_user
    journals = viewing_user.journals.all()
    return render(request, 'my_journals.html',
                {'user': current_user,
                'journals': journals,
                'user': viewing_user,
                "is_logged_in": currently_logged_in}
                )


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
    
    journal_entries = journalobject.entries.all()
    todays_entry = journal_entries.filter(entry_date__date = today)
    return render(request, 'journal_dashboard.html',
                {'user': current_user,
                'journal': journalobject,
                'journal_entries': journal_entries,
                "todays_entry": todays_entry}
                )

@login_required
def view_entry(request, entry_id):
    current_user = request.user

    try:
        entry = Entry.objects.get(id=entry_id)
    except ObjectDoesNotExist:
        return render(request, 'permission_denied.html',)
    
    if entry.owner != current_user:
        return render(request, 'permission_denied.html', {'reason': "You do not own this journal"} )
    
    return render(request, 'view_entry.html', {'user': current_user, 'entry': entry})


@login_required
def create_entry(request, journal_id):
    today = datetime.now().date()
    current_user = request.user

    try:
        journal = Journal.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        return render(request, 'permission_denied.html',{'reason':"journal not exist"})
    
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

    return redirect(f'/journal_dashboard/{journal.id}')

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
            return redirect(f'/journal_dashboard/{entry.journal.id}')
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
    
    journal = entry.journal
    entry.delete()
    return redirect(f'/journal_dashboard/{journal.id}')



@login_required
def view_journal_entries(request, user_id, journal_id):
    current_user = get_object_or_404(User, id = user_id)
    current_journal = Journal.objects.get(id = journal_id)
    is_user_logged_in = current_user == request.user

    if request.method == 'POST':

        filter_form = EntryFilterForm(current_user, request.POST)
        if filter_form.is_valid():
            journal_entries = filter_form.filter_entries(current_journal)
            sort_form = JournalSortForm(request.POST) 
            if sort_form.is_valid():
                sort_order = sort_form.cleaned_data['sort_by_entry_date']
                if sort_order == 'descending':
                    journal_entries = journal_entries.order_by("entry_date")
                    journal_entries = journal_entries.reverse()
                elif sort_order == 'ascending':
                    journal_entries = journal_entries.order_by("entry_date")    

        else:

            sort_form = JournalSortForm()
            journal_entries = current_journal.entries.all()

            if not is_user_logged_in:
                journal_entries = journal_entries.filter(private = False)

            context = {
                    'filter_form': filter_form,
                    'sort_form': sort_form,
                    'journal_entries': journal_entries,
                    'journal_param': my_journals_to_journal_param(journal_entries),
                    'user': current_user,
                    'journal': current_journal,
                    'is_logged_in': is_user_logged_in
                }
            return render(request, 'view_all_journal_entries.html', context)
        
        if not is_user_logged_in:
                journal_entries = journal_entries.filter(private = False)

        context = {
            'filter_form': filter_form,
            'sort_form': sort_form,
            'journal_entries': journal_entries,
            'journal_param': my_journals_to_journal_param(journal_entries),
            'user': current_user,
            'journal': current_journal,
            'is_logged_in': is_user_logged_in
        }
        return render(request, 'view_all_journal_entries.html', context) 

    journal_entries = current_journal.entries.all()

    if not is_user_logged_in:
                journal_entries = journal_entries.filter(private = False)

    filter_form = EntryFilterForm(current_user)
    sort_form = JournalSortForm()
    
    context = {
            'filter_form': filter_form,
            'sort_form': sort_form,
            'journal_entries': journal_entries or False,
            'user': current_user,
            'journal_param': my_journals_to_journal_param(journal_entries),
            'journal': current_journal,
            'is_logged_in': is_user_logged_in
        }
    
    return render(request, 'view_all_journal_entries.html', context)   


def my_journals_to_journal_param(journal_entries):
    journals = []
    for journal in journal_entries:
        journals.append(f"{journal.id}")
    journal_param = ','.join(journals)
    return journal_param

from django.http import JsonResponse, Http404
from django.utils.translation import gettext as _

# Attempt to import the necessary functionalities from the package
# Note: This is hypothetical and depends on the actual package structure
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import image_verify, handle_uploaded_file, NoImageException

def custom_upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        try:
            image_verify(request.FILES["upload"])
        except NoImageException as ex:
            return JsonResponse({"error": {"message": f"{ex}"}})
        if form.is_valid():
            url = handle_uploaded_file(request.FILES["upload"])
            return JsonResponse({"url": url})
    else:
        raise Http404(_("Page not found."))
