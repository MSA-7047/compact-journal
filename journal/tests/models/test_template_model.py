from django.test import TestCase
from django.core.exceptions import ValidationError
from journal.models import Template, User


class TemplateModelTest(TestCase):
     """Unit tests for the template model."""
     
    fixtures = [
        'journal/tests/fixtures/default_user.json',
        'journal/tests/fixtures/other_users.json'
    ]

    def setUp(self) -> None:
        self.user: User = User.objects.get(username='@johndoe')
        self.template: Template = Template.objects.create(
            title="Test Title",
            description="Lorem Ipsum",
            bio="Lorem Ipsum",
            owner=self.user
        )
        return super().setUp()
    
    def _assert_template_is_valid(self, temp: Template, msg: str = None) -> None:
        try:
            temp.full_clean()
        except ValidationError:
            self.fail(msg)

    def _assert_template_is_invalid(self, temp: Template, msg: str = None) -> None:
        with self.assertRaises(ValidationError, msg=msg):
            temp.full_clean()

    def test_template_is_valid(self) -> None:
        self._assert_template_is_valid(
            self.template,
            "Failed default test"
        )
    
    def test_title_can_be_30_long(self) -> None:
        self.template.title = 'a'*30
        self._assert_template_is_valid(
            self.template,
            "Title length was 30, which is supposed to be valid"
        )

    def test_title_cant_be_more_than_30_long(self) -> None:
        self.template.title = 'a'*31
        self._assert_template_is_invalid(
            self.template,
            "Title length was 31, which is supposed to be invalid"
        )

    def test_title_cant_be_blank(self) -> None:
        self.template.title = ''
        self._assert_template_is_invalid(
            self.template,
            "Title was blank, which is supposed to be invalid"
        )

    def test_description_can_be_150_long(self) -> None:
        self.template.description = 'a'*150
        self._assert_template_is_valid(
            self.template,
            "Desctiption length was 1.000, which is supposed to be valid"
        )

    def test_description_can_be_blank(self) -> None:
        self.template.description = ''
        self._assert_template_is_valid(
            self.template,
            "Description was blank, which is supposed to be valid"
        )

    def test_bio_can_be_10000_long(self) -> None:
        self.template.bio = 'a'*10_000
        self._assert_template_is_valid(
            self.template,
            "'Bio' length was 10000, which is supposed to be valid"
        )

    def test_bio_can_be_blank(self) -> None:
        self.template.bio = ''
        self._assert_template_is_invalid(
            self.template,
            "'Bio' was blank, which is supposed to be invalid"
        )

    def test_owner_cant_be_null(self) -> None:
        self.template.owner = None
        self._assert_template_is_invalid(
            self.template,
            "Owner is null, which is supposed to be invalid"
        )