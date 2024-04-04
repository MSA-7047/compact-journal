from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
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

    return export_to_pdf(
        template_src='entry_as_PDF.html',
        context_dict={"entry": entry_instance},
        title=entry_instance.title
    )

def export_journal_as_PDF(request, journal_entries):

    journal_entries_list, journal = unpack_journals(journal_entries)

    return export_to_pdf(
        template_src='journal_as_PDF.html',
        context_dict={"journal_entries": journal_entries_list, "journal": journal},
        title=f'{journal.title} entries'
    )

def export_single_group_entry_as_PDF(request, group_id, journal_id):

    entry = GroupEntry.objects.get(id=journal_id)
    group_ = get_object_or_404(Group, group_id=group_id)

    return export_to_pdf(
        template_src='group_entry_as_PDF.html',
        context_dict={"group": group_, "entry": entry},
        title=f'{group_.name}_{entry.title}'
    )

def export_group_journal_as_PDF(request, group_id):

    group_ = get_object_or_404(Group, group_id=group_id)
    journal_entries = GroupEntry.objects.filter(owner=group_)

    return export_to_pdf(
        template_src='group_journal_as_PDF.html',
        context_dict={"journal_entries": journal_entries,"group": group_},
        title=f'{group_.name}_journals')
    
    #method for actually generating the pdf document
def export_to_pdf(template_src, context_dict,title):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={title}.pdf'
    pisa.CreatePDF(html, dest=response)
    return response

#takes a stringinput which is a comma seperated list of entry IDs and returns the corrosponding
#entry objects in a list
def unpack_journals(journal_entries):
    journals = journal_entries.split(',')
    journal_entries = []
    for journal in journals:
        journal_entries.append(get_object_or_404(Entry, id=int(journal)))
    journal = journal_entries[0].journal
    return journal_entries, journal