from django.test import TestCase
from journal.models import Level, User


class LevelTestCase(TestCase):


    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user, _ = User.objects.get_or_create(username='test_user')
        self.level, _ = Level.objects.get_or_create(user=self.user)

    def test_level_property(self):
        self.assertEqual(self.level.level, self.level.current_level)
        
    def test_calculate_level_with_zero_points(self):
        level_info = self.level.calculate_level(total_points=0)
        self.assertEqual(level_info['current_level'], 1)
        self.assertEqual(level_info['points_to_next_level'], 100)
        self.assertEqual(level_info['points_needed'], 100)

    def test_calculate_level_with_less_than_100_points(self):
        level_info = self.level.calculate_level(total_points=50)
        self.assertEqual(level_info['current_level'], 1)
        self.assertEqual(level_info['points_to_next_level'], 50)
        self.assertEqual(level_info['points_needed'], 100)

    def test_calculate_level_with_100_points(self):
        level_info = self.level.calculate_level(total_points=100)
        self.assertEqual(level_info['current_level'], 2)
        self.assertEqual(level_info['points_to_next_level'], 100)
        self.assertEqual(level_info['points_needed'], 200)

    def test_calculate_level_with_200_points(self):
        level_info = self.level.calculate_level(total_points=200)
        self.assertEqual(level_info['current_level'], 3)
        self.assertEqual(level_info['points_to_next_level'], 100)
        self.assertEqual(level_info['points_needed'], 300)