from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from journal.models import Entry, GroupEntry, Group

def export_single_entry_as_PDF(request, entry_id):

    try:
        entry_instance = Entry.objects.get(id=entry_id)
    except ObjectDoesNotExist:
        messages.warning(request, "You have attempted to access an invalid URL, redirected to dashboard")
        return redirect(reverse('dashboard'))

    # Check if the current user has permission to edit the journal
    if request.user != entry_instance.owner:
        messages.warning(request, "You have attempted to export an entry that is not yours, redirected to dashboard")
        return redirect(reverse('dashboard'))

    template = get_template('entry_as_PDF.html')
    html = template.render({"entry": entry_instance})  # Pass context data if needed
    title = entry_instance.title
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={title}.pdf'
    pisa.CreatePDF(html, dest=response)
    return response

def export_journal_as_PDF(request, journal_entries):

    journals = journal_entries.split(',')
    journal_entries = []
    for journal in journals:
        journal_entries.append(get_object_or_404(Entry, id=int(journal)))
    journal = journal_entries[0].journal
    template = get_template('journal_as_PDF.html')
    html = template.render({"journal_entries": journal_entries, "journal": journal}) 
    title = journal.title  + " entries"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={title}.pdf'
    pisa.CreatePDF(html, dest=response)
    return response

def export_single_group_entry_as_PDF(request, group_id, journal_id):
    entry = GroupEntry.objects.get(id=journal_id)
    group_ = get_object_or_404(Group, group_id=group_id)
    template = get_template('group_entry_as_PDF.html')
    html = template.render({"group": group_, "entry": entry})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={group_.name}_{entry.title}.pdf'
    pisa.CreatePDF(html, dest=response)
    return response

def export_group_journal_as_PDF(request, group_id):
    group_ = get_object_or_404(Group, group_id=group_id)
    journal_entries = GroupEntry.objects.filter(owner=group_)
    template = get_template('group_journal_as_PDF.html')
    html = template.render({"journal_entries": journal_entries, "group": group_})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={group_.name}_journals .pdf'
    pisa.CreatePDF(html, dest=response)
    return response