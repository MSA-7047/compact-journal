from django.test import TestCase
from journal.models import Journal, Entry, User
from journal.forms import EntryFilterForm
from datetime import timedelta
from django.utils import timezone

class EntryFilterFormTest(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json',
                'journal/tests/fixtures/other_users.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(username='@johndoe')
        cls.journal = Journal.objects.create(title='Test Journal', summary='Test summary', private=False, owner=cls.user )
        cls.entry1 = Entry.objects.create(title='Entry 1', summary='Summary 1', content='Content 1', mood='Happy', owner=cls.user, journal=cls.journal)
        cls.entry2 = Entry.objects.create(title='Entry 2', summary='Summary 2', content='Content 2', mood='Sad', owner=cls.user, journal=cls.journal)
        cls.entry3 = Entry.objects.create(title='Entry 3', summary='Summary 3', content='Content 3', mood='Angry', owner=cls.user, journal=cls.journal)

    def test_filter_entries_by_entry_date(self):
        form_data = {'entry_date': '24h'}
        form = EntryFilterForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())  # Ensure form is valid before accessing cleaned_data
        filtered_entries = form.filter_entries(journal=self.journal).order_by('id')
        expected_entries = Entry.objects.filter(entry_date__gte=timezone.now() - timedelta(days=1), journal=self.journal).order_by('id')
        self.assertQuerysetEqual(filtered_entries, expected_entries, transform=lambda x: x)

    def test_filter_entries_by_mood(self):
        form_data = {'mood': 'Happy'}
        form = EntryFilterForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())  # Ensure form is valid before accessing cleaned_data
        filtered_entries = form.filter_entries(journal=self.journal)
        expected_entries = Entry.objects.filter(mood='Happy', journal=self.journal)
        self.assertQuerysetEqual(filtered_entries, expected_entries, transform=lambda x: x)

    def test_filter_entries_by_title_search(self):
        form_data = {'title_search': 'Entry 1'}
        form = EntryFilterForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())  # Ensure form is valid before accessing cleaned_data
        filtered_entries = form.filter_entries(journal=self.journal)
        expected_entries = Entry.objects.filter(title__icontains='Entry 1', journal=self.journal)
        self.assertQuerysetEqual(filtered_entries, expected_entries, transform=lambda x: x)

    def test_filter_entries_no_filters(self):
        form_data = {}
        form = EntryFilterForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())  # Ensure form is valid before accessing cleaned_data
        filtered_entries = form.filter_entries(journal=self.journal).order_by('id')
        expected_entries = Entry.objects.filter(journal=self.journal).order_by('id')
        self.assertQuerysetEqual(filtered_entries, expected_entries, transform=lambda x: x)




