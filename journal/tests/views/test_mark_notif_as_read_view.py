from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from journal.models import Notification


class MarkNotificationAsReadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.notification = Notification.objects.create(
            message="Test notification message",
            user=self.user
        )

    def test_mark_notification_as_read(self):
        response = self.client.get(reverse('mark_notification_as_read', args=[self.notification.id]))
        self.assertEqual(response.status_code, 302)  # Check if the view redirects after marking notification as read
        self.notification.refresh_from_db()  # Refresh the notification instance from the database
        self.assertTrue(self.notification.is_read)  # Check if the notification is marked as read
        time = self.notification.time_created.strftime("%Y-%m-%d %H:%M:%S")
        storage = get_messages(response.wsgi_request)
        success_message = None
        for message in storage:
            if message.tags == 'success':
                success_message = message
                break
        self.assertIsNotNone(success_message)  # Check if a success message is returned
        self.assertEqual(success_message.message, f"Notification for the Test Notification created at {time} was marked as read.")  # Check if the success message is correct
