
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from journal.models import Entry

def view_PDF(request, journal_id):
    current_user = request.user
    try:
        journal = Entry.objects.get(id=journal_id)
    except ObjectDoesNotExist:
        return render(request, 'permission_denied.html',)
    if journal.journal_owner != current_user:
        return render(request, 'permission_denied.html', {'reason': "You do not own this journal"} )
    template = get_template('journalPDF.html')
    html = template.render({"journal": journal})  # Pass context data if needed
    title = journal.journal_title
    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={title}'

    # Generate PDF from HTML content
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF: %s' % pisa_status.err)

    return response

def view_PDF_list(request, myJournals):
    # Split the string into a list
    journals = myJournals.split(',')
    myJournals = []
    for journal in journals:
        myJournals.append(get_object_or_404(Entry, id=int(journal)))
    template = get_template('myJournalsPDF.html')
    html = template.render({"myJournals": myJournals})  # Pass context data if needed
    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=title'
    # Generate PDF from HTML content
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF: %s' % pisa_status.err)

    return response

    for y in x:
        print(y.journal_title)  # Just for demonstration
    
    # Further processing of the journals as needed
    
    return HttpResponse('PDF generation view')

