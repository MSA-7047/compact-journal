from django.test import TestCase
from django.contrib.auth import get_user_model
from journal.models import GroupEntry, Group

User = get_user_model()

class GroupEntryModelTest(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json']


    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.group = Group.objects.create(name='Test Group')

    def test_group_entry_creation(self):
        # Create a GroupEntry instance
        entry = GroupEntry.objects.create(
            title='Test Entry',
            summary='This is a test summary.',
            content='This is the content of the test entry.',
            mood='Happy',
            owner=self.group,
            last_edited_by=self.user
        )

        # Retrieve the created entry from the database
        retrieved_entry = GroupEntry.objects.get(pk=entry.pk)

        # Assert that the retrieved entry matches the created entry
        self.assertEqual(retrieved_entry.title, 'Test Entry')
        self.assertEqual(retrieved_entry.summary, 'This is a test summary.')
        self.assertEqual(retrieved_entry.content, 'This is the content of the test entry.')
        self.assertEqual(retrieved_entry.mood, 'Happy')
        self.assertEqual(retrieved_entry.owner, self.group)
        self.assertEqual(retrieved_entry.last_edited_by, self.user)

    def test_group_entry_fields(self):
        # Assert that the fields have the expected attributes
        entry = GroupEntry()
        self.assertEqual(entry._meta.get_field('title').verbose_name, 'Title')
        self.assertEqual(entry._meta.get_field('summary').max_length, 200)
        # Add assertions for other fields as needed

   
