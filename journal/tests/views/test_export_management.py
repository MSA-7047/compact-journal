from django.test import TestCase, RequestFactory, Client
from django.http import HttpRequest
from django.urls import reverse
from journal.views.export_management import *
from journal.models import Entry, User, Journal

class PDFExportViewTest(TestCase):


    fixtures = [
        'journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username='@johndoe', password='Password123')
        self.journal = Journal.objects.create(title='Test Journal', summary='Journal Summary', owner=self.user, private=True)
        self.journal_entry = Entry.objects.create(owner=self.user, title='Journal Entry 1', summary='Journal Summary 1', content='Journal Content 1', journal=self.journal, private=True)
        self.group = Group.objects.create(name='Test Group')
        self.group_entry = GroupEntry.objects.create(
            title='Test Entry',
            content='Test content',
            mood='Angry',
            owner=self.group
        )

    def test_export_single_entry_as_PDF(self):
        request = self.factory.get('/export-entry-pdf/1/')
        request.user = self.user
        response = export_single_entry_as_PDF(request, entry_id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename=Journal Entry 1.pdf')

    def test_export_single_entry_as_PDF_invalid_login(self):
        self.client.logout()
        request = self.factory.get('/export-entry-pdf/1/')
        request.user = self.user
        response = export_single_entry_as_PDF(request, entry_id=1)
        self.assertEqual(response.status_code, 200)

    def test_export_journal_as_PDF(self):
        id = self.journal_entry.id
        request = self.factory.get(f'/export-journal-pdf/{id}/')
        request.user = self.user
        response = export_journal_as_PDF(request, journal_entries='1')
        self.assertEqual(response.status_code, 200)
<<<<<<< HEAD
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename=Test Journal entries.pdf')
=======
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename=Test Journal entries')

    def test_export_single_group_entry_as_PDF(self):
        request = RequestFactory().get(reverse('export_single_group_entry', args=[self.group.group_id, self.group_entry.id]))
        request.user = self.user

        response = export_single_group_entry_as_PDF(request, self.group.group_id, self.group_entry.id)

        self.assertIsInstance(response, HttpResponse)

        self.assertEqual(response['Content-Type'], 'application/pdf')

        expected_filename = f'{self.group.name}_{self.group_entry.title}.pdf'
        self.assertTrue(expected_filename in response['Content-Disposition'])

    def test_export_group_journal_as_PDF(self):
        request = RequestFactory().get(reverse('export_group_journal', args=[self.group.group_id]))
        request.user = self.user

        response = export_group_journal_as_PDF(request, self.group.group_id)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response['Content-Type'], 'application/pdf')
>>>>>>> 77ad5f4 (add group_journal_to_pdf in export_management)
