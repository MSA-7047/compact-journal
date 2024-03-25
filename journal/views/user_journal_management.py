from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.detail import DetailView

from journal.models import *
from journal.forms import *

# class JournalDetail(DetailView):
#     model = Journal
#     template_name = 'journal_detail.html'

#     def get_object(self, queryset=None):
#         journal_id = self.kwargs.get('journal_id')
#         queryset = self.get_queryset().filter(id=journal_id)
#         obj = queryset.first()
#         return obj


def journal_detail_view(request, journalID):
    # Retrieve the journal object based on the journal_id
    current_user = request.user
    journal = Journal.objects.get(id=journalID)

    # Pass the journal object to the template context
    return render(request, 'journal_detail.html', {'user': current_user, 'journal': journal})


@login_required
def create_journal(request):
    today = datetime.now().date()

    form = CreateJournalForm()
    if request.method != 'POST':
        return render(request, 'create_journal.html', {'form': form})

    form = CreateJournalForm(request.POST)
    if not form.is_valid():
        return render(request, 'create_journal.html', {'form': form})

    journal = Journal.objects.create(
        journal_title=form.cleaned_data.get("journal_title"),
        journal_description=form.cleaned_data.get("journal_description"),
        journal_bio=form.cleaned_data.get("journal_bio"),
        journal_mood=form.cleaned_data.get("journal_mood"),
        journal_owner=request.user
    )
    journal.save()

    return redirect('/dashboard/')



@login_required
def EditJournal(request, journalID): 

    journal = get_object_or_404(Journal, id=journalID)

    if request.method == 'POST':
        form = CreateJournalForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the detail view of the edited journal
    else:
        form = CreateJournalForm(instance=journal)

    return render(request, 'create_journal.html', {'form': form, 'journal': journal, 'title': "Update Journal"})


@login_required
def DeleteJournal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    journal.delete()
    return redirect('dashboard')




# @login_required
# def all_journal_entries_view(request):
#     current_user = request.user
#     journal_existence = Journal.objects.filter(journal_title__isnull=False)
#     return render(request, 'all_entries.html', { 'user': current_user,  'journal_existence': journal_existence or False})


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
            myJournals = Journal.objects.filter(journal_owner=current_user)
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
    
    myJournals = Journal.objects.filter(journal_owner=current_user)

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