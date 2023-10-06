import unittest
from datetime import datetime
import sys
sys.path.append('../src/')
from src.windowing import get_next_window, get_current_window, TimeUnit

class TestCurrentWindow(unittest.TestCase):
        
    def test_get_current_window_minutes(self):
        now = datetime(2023, 10, 3, 12, 15, 15)
        start, stop = get_current_window(1, TimeUnit.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12, 15, 0))
        self.assertEqual(stop, datetime(2023, 10, 3, 12, 16, 0))

        now = datetime(2023, 10, 3, 0, 1)

  
        start, stop = get_current_window(10, TimeUnit.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 3, 0, 10))

        now = datetime(2023, 10, 3, 12, 15)
        start, stop = get_current_window(70, TimeUnit.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12, 0))
        self.assertEqual(stop, datetime(2023, 10, 3, 13, 10)) 

    def test_get_current_window_hours(self):
        now = datetime(2023, 10, 3, 12, 15, 15)
        start, stop = get_current_window(1, TimeUnit.HOURS, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 3, 13, 0, 0))     

    def test_get_current_window_days(self):
        now = datetime(2023, 10, 3, 12, 15, 15)
        start, stop = get_current_window(1, TimeUnit.DAYS, now)
        self.assertEqual(start, datetime(2023, 10, 3, 0, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 4, 0, 0, 0)) 

    def test_get_current_window_days_cross_year(self):
        now = datetime(2023, 12, 31, 12, 15, 15)
        start, stop = get_current_window(2, TimeUnit.DAYS, now)
        self.assertEqual(start, datetime(2023, 12, 31, 0, 0, 0))
        self.assertEqual(stop, datetime(2024, 1, 2, 0, 0, 0)) 

    def test_get_current_window_hours_cross_day(self):
        now = datetime(2023, 10, 3, 23, 15, 15)
        start, stop = get_current_window(3, TimeUnit.HOURS, now)
        self.assertEqual(start, datetime(2023, 10, 3, 23, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 4, 2, 0, 0))

    def test_bad_intervals(self):
        self.assertRaises(ValueError, get_current_window, -1, TimeUnit.HOURS)
        self.assertRaises(TypeError, get_current_window, 0.0, TimeUnit.HOURS)

if __name__ == '__main__':
    unittest.main()


