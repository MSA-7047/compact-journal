from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from journal.models import Notification, User


class MarkNotificationAsReadTestCase(TestCase):

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username='@johndoe', password='Password123')
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
        self.assertEqual(success_message.message, f"Notification created at {time} was marked as read.")  # Check if the success message is correct

    def test_mark_all_notification_as_read(self):
        notification1 = Notification.objects.create(user=self.user, message='Test Notification 1', notification_type='info')
        notification2 = Notification.objects.create(user=self.user, message='Test Notification 2', notification_type='info')
        response = self.client.post(reverse('mark_all_notification_as_read'))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after marking all notifications as read
        notification1.refresh_from_db()
        notification2.refresh_from_db()
        self.assertTrue(notification1.is_read)
        self.assertTrue(notification2.is_read)


