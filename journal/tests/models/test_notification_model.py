from django.test import TestCase
from django.core.exceptions import ValidationError
from journal.models import Notification, User


class NotificationModelTest(TestCase):
    """"""

    fixtures = [
        'journal/tests/fixtures/default_user.json',
        'journal/tests/fixtures/other_users.json'
    ]

    def setUp(self) -> None:
        self.user: User = User.objects.get(username='@johndoe')
        self.notif: Notification = Notification.objects.create(
            message="Test",
            user=self.user
        )
        return super().setUp()
    
    def _assert_notification_is_valid(self, notif: Notification, msg: str = None) -> None:
        try:
            notif.full_clean()
        except ValidationError:
            self.fail(msg)

    def _assert_notification_is_invalid(self, notif: Notification, msg: str = None) -> None:
        with self.assertRaises(ValidationError, msg=msg):
            notif.full_clean()

    def test_notification_is_valid(self) -> None:
        self._assert_notification_is_valid(
            self.notif,
            "Failed default test"
        )

    def test_user_cannot_be_null(self) -> None:
        self.notif.user = None
        self._assert_notification_is_invalid(
            self.notif,
            "User is decalared null and should be invalid"
        )
