from django.test import TestCase
from django.conf import settings
from journal.models import UserMessage, User

class UserMessageTestCase(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json']


    def setUp(self):
        # Create a test user
        self.user = User.objects.get(username='@johndoe')

    def test_user_message_creation(self):
        # Create a user message
        message_text = "This is a test message."
        user_message = UserMessage.objects.create(user=self.user, message=message_text)

        # Check if the message was created successfully
        self.assertEqual(user_message.user, self.user)
        self.assertEqual(user_message.message, message_text)
        self.assertFalse(user_message.read)

    def test_message_read_status(self):
        # Create a user message
        message_text = "This is another test message."
        user_message = UserMessage.objects.create(user=self.user, message=message_text)

        # Check initial read status
        self.assertFalse(user_message.read)

        # Mark the message as read
        user_message.read = True
        user_message.save()

        # Check if the message read status was updated
        updated_user_message = UserMessage.objects.get(pk=user_message.pk)
        self.assertTrue(updated_user_message.read)