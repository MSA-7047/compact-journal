from django.test import TestCase
from journal.models import Journal, User
from django.utils import timezone

class JournalModelTest(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json']
                
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.user = User.objects.get(username='@johndoe')
        self.journal = Journal.objects.create(
            title='Test Journal',
            summary='This is a test journal summary.',
            entry_date=timezone.now(),
            private=False,
            owner=self.user
        )

    def test_title_label(self):
        field_label = self.journal._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Title')

    def test_summary_label(self):
        field_label = self.journal._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'Description')

    def test_summary_max_length(self):
        max_length = self.journal._meta.get_field('summary').max_length
        self.assertEqual(max_length, 500)

    def test_owner_relation(self):
        owner = self.journal.owner
        self.assertEqual(owner.username, '@johndoe')

    def test_private_default_value(self):
        self.assertFalse(self.journal.private)
