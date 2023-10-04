import unittest
from datetime import datetime
import sys
sys.path.append('../src/')
from src.windowing import get_next_window, get_current_window, IntervalType

class TestCurrentWindow(unittest.TestCase):
        
    def test_get_current_window_minutes(self):
        now = datetime(2023, 10, 3, 12, 15, 15)
        start, stop = get_current_window(1, IntervalType.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12, 15, 0))
        self.assertEqual(stop, datetime(2023, 10, 3, 12, 16, 0))

    def test_get_current_window_hours(self):
        now = datetime(2023, 10, 3, 12, 15, 15)
        start, stop = get_current_window(1, IntervalType.HOURS, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 3, 13, 0, 0))     

    def test_get_current_window_hours_cross_day(self):
        now = datetime(2023, 10, 3, 23, 15, 15)
        start, stop = get_current_window(3, IntervalType.HOURS, now)
        self.assertEqual(start, datetime(2023, 10, 3, 23, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 4, 2, 0, 0))

if __name__ == '__main__':
    unittest.main()


