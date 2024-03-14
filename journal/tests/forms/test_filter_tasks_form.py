from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from journal.forms import JournalFilterForm
from journal.models import Journal
from journal.models import User

class JournalFilterFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.journal1 = Journal.objects.create(journal_title='Test Journal 1', journal_mood='Happy', entry_date=timezone.now(), journal_owner=self.user)
        self.journal2 = Journal.objects.create(journal_title='Test Journal 2', journal_mood='Sad', entry_date=timezone.now() - timedelta(days=2), journal_owner=self.user)

    def test_no_filter(self):
        form = JournalFilterForm(user=self.user, data={})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        all_journals = Journal.objects.all()
        filtered_journals = form.filter_tasks()
        self.assertQuerysetEqual(all_journals, filtered_journals, ordered=False)

    def test_filter_by_title_contains(self):
        form = JournalFilterForm(user=self.user, data={'title_contains': 'Test Journal 1'})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        filtered_journals = form.filter_tasks()
        self.assertIn(self.journal1, filtered_journals)
        self.assertNotIn(self.journal2, filtered_journals)

    def test_filter_by_mood(self):
        form = JournalFilterForm(user=self.user, data={'mood': 'Happy'})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        filtered_journals = form.filter_tasks()
        self.assertIn(self.journal1, filtered_journals)
        self.assertNotIn(self.journal2, filtered_journals)

    def test_filter_by_entry_date_24h(self):
        form = JournalFilterForm(user=self.user, data={'entry_date': '24h'})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        filtered_journals = form.filter_tasks()
        self.assertIn(self.journal1, filtered_journals)
        self.assertNotIn(self.journal2, filtered_journals)

    def test_filter_by_entry_date_3d(self):
        form = JournalFilterForm(user=self.user, data={'entry_date': '3d'})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        filtered_journals = form.filter_tasks()
        self.assertNotIn(self.journal1, filtered_journals)
        self.assertIn(self.journal2, filtered_journals)

    def test_filter_by_entry_date_1w(self):
        form = JournalFilterForm(user=self.user, data={'entry_date': '1w'})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        filtered_journals = form.filter_tasks()
        self.assertNotIn(self.journal1, filtered_journals)
        self.assertNotIn(self.journal2, filtered_journals)

    def test_filter_by_entry_date_1m(self):
        form = JournalFilterForm(user=self.user, data={'entry_date': '1m'})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        filtered_journals = form.filter_tasks()
        self.assertNotIn(self.journal1, filtered_journals)
        self.assertNotIn(self.journal2, filtered_journals)

    def test_filter_by_entry_date_6m_plus(self):
        form = JournalFilterForm(user=self.user, data={'entry_date': '6m+'})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        filtered_journals = form.filter_tasks()
        self.assertIn(self.journal1, filtered_journals)
        self.assertIn(self.journal2, filtered_journals)

    def test_invalid_entry_date(self):
        form = JournalFilterForm(user=self.user, data={'entry_date': 'invalid'})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        filtered_journals = form.filter_tasks()
        self.assertNotIn(self.journal1, filtered_journals)
        self.assertNotIn(self.journal2, filtered_journals)

    def test_multiple_filters(self):
        form = JournalFilterForm(user=self.user, data={'title_contains': 'Test Journal 1', 'mood': 'Happy', 'entry_date': '24h'})
        self.assertTrue(form.is_valid())  # Validate the form before accessing cleaned_data
        filtered_journals = form.filter_tasks()
        self.assertIn(self.journal1, filtered_journals)
        self.assertNotIn(self.journal2, filtered_journals)





