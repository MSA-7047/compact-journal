from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.detail import DetailView

from journal.models import *


class JournalDetail(DetailView):
    model = Journal
    template_name = 'journal_detail.html'

    def get_object(self, queryset=None):
        journal_id = self.kwargs.get('journal_id')
        queryset = self.get_queryset().filter(id=journal_id)
        obj = queryset.first()
        return obj


def journal_detail_view(request, journal_id):
    # Retrieve the journal object based on the journal_id
    current_user = request.user
    journal = Journal.objects.get(id=journal_id)

    # Pass the journal object to the template context
    return render(request, 'journal_detail.html', {'user': current_user, 'journal': journal})


@login_required
def create_journal(request):
    today = datetime.now().date()

    form = CreateJournalForm()
    if request.method != 'POST':
        return render(request, 'add_journal.html', {'form': form})

    form = CreateJournalForm(request.POST)
    if not form.is_valid():
        return render(request, 'add_journal.html', {'form': form})

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
def ChangeJournalInfo(request, journalID):
    journal = get_object_or_404(Journal, id=journalID)

    if request.method == 'POST':
        form = EditJournalInfoForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the detail view of the edited journal
    else:
        form = EditJournalInfoForm(instance=journal)

    return render(request, 'change_journal_info.html', {'form': form, 'journal': journal})


@login_required
def DeleteJournal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    journal.delete()
    return redirect('dashboard')


@login_required
def ChangeJournalDescription(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)

    if request.method == 'POST':
        form = EditJournalDescriptionForm(request.POST, instance=journal)
        if form.is_valid():
            new_description = form.cleaned_data['journal_description']
            journal.journal_description = new_description
            journal.save()
            return redirect('all_entries')
    else:
        form = EditJournalDescriptionForm(instance=journal)

    return render(request, 'change_journal_description.html', {'form': form, 'journal': journal})


@login_required
def all_journal_entries_view(request):
    current_user = request.user
    journal_existence = Journal.objects.filter(journal_title__isnull=False)
    return render(request, 'all_entries.html', { 'user': current_user,  'journal_existence': journal_existence or False})


@login_required
def my_journals_view(request):
    current_user = request.user
    if request.method == 'POST':
        filter_form = JournalFilterForm(current_user, request.POST)
        if not filter_form.is_valid():
            sort_form = JournalSortForm()
            context = {
                'filter_form': filter_form,
                'sort_form': sort_form,
                'show_alert': True,
                'myJournals': Journal.objects.filter(journal_owner=current_user)
            }
            return render(request, 'My_Journals.html', context)

        my_journals = filter_form.filter_tasks()
        my_journals = my_journals.filter(journal_owner=current_user)

        sort_form = JournalSortForm(request.POST)
        if sort_form.is_valid():
            sort_order = sort_form.cleaned_data['sort_by_entry_date']
            if sort_order == 'descending':
                my_journals = my_journals.order_by("entry_date")
                my_journals = my_journals.reverse()
            elif sort_order == 'ascending':
                my_journals = my_journals.order_by("entry_date")

        context = {
            'filter_form': filter_form,
            'sort_form': sort_form,
            'myJournals': my_journals
        }
        return render(request, 'my_journals.html', context)

    myjournals = Journal.objects.filter(journal_owner=current_user)
    filter_form = JournalFilterForm(current_user)
    sort_form = JournalSortForm()

    context = {
            'filter_form': filter_form,
            'sort_form': sort_form,
            'myJournals': myjournals or False,
            'user': current_user
        }

    return render(request, 'my_journals.html', context)
