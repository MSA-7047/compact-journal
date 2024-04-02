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
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename=Test Journal entries.pdf')

    def test_export_single_group_entry_as_PDF(self):
        url = reverse('export_single_group_entry', kwargs={'group_id': self.group.group_id, 'journal_id': self.group_entry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content)  # Ensure content is not empty

    def test_export_group_journal_as_PDF(self):
        url = reverse('export_group_journal', kwargs={'group_id': self.group.group_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content)  # Ensure content is not empty
