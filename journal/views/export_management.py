

from django.http import HttpResponse
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.conf import settings
from journal.models import Journal

def view_PDF(request, journal_id):
    # Fetch data from your Django model or pass data to template context
    journal = get_object_or_404(Journal, id=journal_id)
    # Load the HTML template
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
        myJournals.append(get_object_or_404(Journal, id=int(journal)))
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

