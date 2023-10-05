import unittest
from datetime import datetime
import sys
sys.path.append('../src/')
from src.windowing import get_next_window, get_current_window, IntervalType

class TestNextWindow(unittest.TestCase):

    def test_get_next_window_minutes(self):
        now = datetime(2023, 10, 3, 12, 15)

        # Test minutes
        start, stop = get_next_window(1, IntervalType.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12, 16))
        self.assertEqual(stop, datetime(2023, 10, 3, 12, 17))

        start, stop = get_next_window(10, IntervalType.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12, 20))
        self.assertEqual(stop, datetime(2023, 10, 3, 12, 30))

        start, stop = get_next_window(70, IntervalType.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 13, 10))
        self.assertEqual(stop, datetime(2023, 10, 3, 14, 20))

    def test_get_next_window_hours(self):
        now = datetime(2023, 10, 3, 12, 15)
        
        start, stop = get_next_window(1, IntervalType.HOURS, now)
        self.assertEqual(start, datetime(2023, 10, 3, 13, 0))
        self.assertEqual(stop, datetime(2023, 10, 3, 14, 0))

        start, stop = get_next_window(10, IntervalType.HOURS, now)
        self.assertEqual(start, datetime(2023, 10, 3, 22, 0))
        self.assertEqual(stop, datetime(2023, 10, 4, 8, 0))

    def test_get_next_window_days(self):
        now = datetime(2023, 10, 3, 12, 15)

        # Test minutes
        start, stop = get_next_window(1, IntervalType.DAYS, now)
        self.assertEqual(start, datetime(2023, 10, 4, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 5, 0, 0))

        start, stop = get_next_window(7, IntervalType.DAYS, now)
        self.assertEqual(start, datetime(2023, 10, 10, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 17, 0, 0))

    def test_bad_intervals(self):
        self.assertRaises(ValueError, get_current_window, -1, IntervalType.HOURS)
        self.assertRaises(TypeError, get_current_window, 0.0, IntervalType.HOURS)

    def test_get_next_window_cross_days(self):
        now = datetime(2023, 10, 3, 23, 59)
        start, stop = get_next_window(15, IntervalType.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 4, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 4, 0, 15))
        
if __name__ == '__main__':
    unittest.main()


