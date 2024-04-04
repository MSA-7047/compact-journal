from django.test import TestCase
from journal.models import Points, User

class PointsTestCase(TestCase):
    """Unit tests for the Points model."""
    fixtures = [
        'journal/tests/fixtures/default_user.json']
    
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.points = Points.objects.create(
            user=self.user,
            points=100,
            description='Test points'
        )

    def test_str_method(self):
        expected_str = f"{self.user}'s points"
        self.assertEqual(str(self.points), expected_str)