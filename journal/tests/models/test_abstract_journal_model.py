from django.test import TestCase
from journal.models.AbstractJournal import AbstractJournal
from django.core.exceptions import ValidationError


class AbstractJournalModelTest(TestCase):
    """Test Class to test the validity of AbstractJournal Model Class"""

    def setUp(self) -> None:
        """"""
        self.abs_journal: AbstractJournal = AbstractJournal.objects.create(
            journal_title="Lorem ipsum",
            journal_description="Lorem ipsum",
            journal_bio="Lorem ipsum",
            journal_mood="Neutral"
        )

    def _assert_journal_is_valid(self, journal: AbstractJournal, msg: str = None) -> None:
        """"""
        try:
            journal.full_clean()
        except ValidationError:
            self.fail(msg)

    def _assert_journal_is_invalid(self, journal: AbstractJournal, msg: str = None) -> None:
        """"""
        with self.assertRaises(ValidationError, msg=msg):
            journal.full_clean()

    def test_journal_is_valid(self) -> None:
        """"""
        self._assert_journal_is_valid(
            self.abs_journal, 
            "Test journal failed default test"
        )

    def test_title_should_be_less_than_or_eq_50(self) -> None:
        """"""
        self.abs_journal.journal_title = 'a'*50
        self._assert_journal_is_valid(
            self.abs_journal, 
            "Journal has 50 characters, which isn't supposed to exceed the maximum length"
        )

    def test_title_should_not_exceed_50(self) -> None:
        """"""
        self.abs_journal.journal_title = 'a'*51
        self._assert_journal_is_invalid(
            self.abs_journal, 
            "Journal has 51 characters, which is supposed to exceed the maximum length"
        )
    
    def test_title_should_not_be_blank(self) -> None:
        """"""
        self.abs_journal.journal_title = ''
        self._assert_journal_is_invalid(
            self.abs_journal,
            "Journal title shouldn't be empty, but is"
        )

    def test_description_should_be_less_than_or_eq_1000(self) -> None:
        """"""
        self.abs_journal.journal_description = 'a' * 1_000
        self._assert_journal_is_valid(
            self.abs_journal,
            "Journal description has 1,000 characters, which isn't supposed to exceed the max length"
        )

    def test_description_should_not_exceed_1000(self) -> None:
        """"""
        self.abs_journal.journal_description = 'a' * 1_001
        self._assert_journal_is_invalid(
            self.abs_journal,
            "Journal description has 1,001 characters, which is supposed to exceed the max_length"
        )

    def test_description_may_not_be_blank(self) -> None:
        """"""
        self.abs_journal.journal_description = ''
        self._assert_journal_is_invalid(
            self.abs_journal,
            "Journal description is empty, which should be invalid"
        )
    
    def test_bio_should_be_less_than_or_eq_10000(self) -> None:
        """"""
        self.abs_journal.journal_bio = 'a' * 10_000
        self._assert_journal_is_valid(
            self.abs_journal,
            "Journal 'bio' has 10,000 characters, which isn't supposed to exceed the max_length"
        )

    def test_bio_should_not_exceed_10000(self) -> None:
        """"""
        self.abs_journal.journal_bio = 'a' * 10_001
        self._assert_journal_is_invalid(
            self.abs_journal,
            "Journal bio has 10,001 characters, which is supposed to exceed the max_length"
        )

    def test_bio_may_not_be_blank(self) -> None:
        """"""
        self.abs_journal.journal_bio = ''
        self._assert_journal_is_invalid(
            self.abs_journal,
            "Journal bio is empty, which should be invalid"
        )

    def test_mood_can_be_happy(self) -> None:
        self.abs_journal.journal_mood = 'Happy'
        self._assert_journal_is_valid(
            self.abs_journal,
            "Journal mood is 'Happy', which is supposed to be a valid mood"
        )

    def test_mood_can_be_sad(self) -> None:
        self.abs_journal.journal_mood = 'Sad'
        self._assert_journal_is_valid(
            self.abs_journal,
            "Journal mood is 'Sad', which is supposed to be a valid mood"
        )

    def test_mood_can_be_angry(self) -> None:
        self.abs_journal.journal_mood = 'Angry'
        self._assert_journal_is_valid(
            self.abs_journal,
            "Journal mood is 'Angry', which is supposed to be a valid mood"
        )

    def test_mood_can_be_neutral(self) -> None:
        self.abs_journal.journal_mood = 'Neutral'
        self._assert_journal_is_valid(
            self.abs_journal,
            "Journal mood is 'Neutral', which is supposed to be a valid mood"
        )

    def test_mood_cant_be_anything_else(self) -> None:
        self.abs_journal.journal_mood = 'Chaotic'
        self._assert_journal_is_invalid(
            self.abs_journal,
            "Journal mood is 'Chaotic', which is supposed to be an invalid mood"
        )

    def test_mood_cant_be_empty(self) -> None:
        self.abs_journal.journal_mood = ''
        self._assert_journal_is_invalid(
            self.abs_journal,
            "Journal mood is blank, which is supposed to be invalid"
        )
