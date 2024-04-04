from django.test import TestCase
from django.core.exceptions import ValidationError
from journal.models import GroupEntry, Group, User, Journal
from django.utils import timezone


class GroupEntryModelTest(TestCase):
    """Unit tests for GroupEntry Model Class"""

    fixtures = ["journal/tests/fixtures/default_user.json"]

    def setUp(self) -> None:
        self.user: User = User.objects.get(username="@johndoe")
        self.group: Group = Group.objects.create(name="Test")
        self.entry: GroupEntry = GroupEntry.objects.create(
            title="Test Entry",
            summary="This is a test Entry summary.",
            content="This is a test Entry content.",
            mood="Happy",
            owner=self.group,
            last_edited_by=self.user
        )

    def _assert_entry_is_valid(self, entry: GroupEntry, msg: str = None) -> None:
        """"""
        try:
            entry.full_clean()
        except ValidationError:
            self.fail(msg)

    def _assert_entry_is_invalid(self, entry: GroupEntry, msg: str = None) -> None:
        """"""
        with self.assertRaises(ValidationError, msg=msg):
            entry.full_clean()

    def test_entry_creation(self):
        self._assert_entry_is_valid(self.entry)

    def test_title_can_be_upto_30(self):
        self.entry.title = "a"*30
        self._assert_entry_is_valid(self.entry)

    def test_title_can_not_exceed_30(self):
        self.entry.title = "a"*31
        self._assert_entry_is_invalid(self.entry)

    def test_summary_can_be_upto_200(self):
        self.entry.summary = "a"*200
        self._assert_entry_is_valid(self.entry)

    def test_summary_can_not_exceed_200(self):
        self.entry.summary = "a"*201
        self._assert_entry_is_invalid(self.entry)

    def test_content_can_be_upto_10000(self):
        self.entry.content = "a"*10_000
        self._assert_entry_is_valid(self.entry)

    def test_content_can_not_exceed_10000(self):
        self.entry.content = "a"*10_001
        self._assert_entry_is_invalid(self.entry)

    def test_all_valid_moods(self):
        MOOD_OPTIONS = [
            ("Sad", "Sad"),
            ("Happy", "Happy"),
            ("Angry", "Angry"),
            ("Neutral", "Neutral"),
            ("Excited", "Excited"),
            ("Confused", "Confused"),
            ("Surprised", "Surprised"),
            ("Hopeful", "Hopeful"),
            ("Frustrated", "Frustrated"),
            ("Grateful", "Grateful"),
            ("Relaxed", "Relaxed"),
            ("Optimistic", "Optimistic"),
            ("Anxious", "Anxious"),
        ]
        for mood, _ in MOOD_OPTIONS:
            self.entry.mood = mood
            self._assert_entry_is_valid(self.entry, msg=f"{mood} failed")

    def test_mood_cannot_be_blank(self):
        self.entry.mood = ""
        self._assert_entry_is_invalid(self.entry)

    def test_mood_cannot_be_an_invalid_mood(self):
        self.entry.mood = "Invalid Mood"
        self._assert_entry_is_invalid(self.entry)

    def test_last_edited_by_can_be_null(self):
        self.entry.last_edited_by = None
        self._assert_entry_is_valid(self.entry)

    def test_owner_cannot_be_null(self):
        self.entry.owner = None
        self._assert_entry_is_invalid(self.entry)
