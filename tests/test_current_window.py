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

        now = datetime(2023, 10, 3, 12, 2, 2)
        start, stop = get_current_window(10, TimeUnit.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12 , 0))
        self.assertEqual(stop, datetime(2023, 10, 3, 12, 10))

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

    def test_current_window_months(self):
        now = datetime(2023, 10, 1, 12, 15, 15)
        start, stop = get_current_window(1, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2023, 10, 1, 0, 0, 0))
        self.assertEqual(stop, datetime(2023, 11, 1, 0, 0, 0))

    def test_month_alignment(self):
        now = datetime(2023, 2, 5, 12, 15, 15)
        start, stop = get_current_window(3, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2023, 1, 1, 0, 0, 0))
        self.assertEqual(stop, datetime(2023, 4, 1, 0, 0, 0))

        now = datetime(2023, 5, 5, 12, 15, 15)
        start, stop = get_current_window(3, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2023, 4, 1, 0, 0, 0))
        self.assertEqual(stop, datetime(2023, 7, 1, 0, 0, 0))

        now = datetime(2023, 9, 5, 12, 15, 15)
        start, stop = get_current_window(3, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2023, 7, 1, 0, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 1, 0, 0, 0))

        now = datetime(2023, 10, 5, 12, 15, 15)
        start, stop = get_current_window(3, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2023, 10, 1, 0, 0, 0))
        self.assertEqual(stop, datetime(2024, 1, 1, 0, 0, 0))

    def test_deal_with_february(self):
        now = datetime(2023, 1, 15, 12, 15, 15)
        start, stop = get_current_window(1, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2023, 1, 1, 0, 0, 0))
        self.assertEqual(stop, datetime(2023, 2, 1, 0, 0, 0))        

        start, stop = get_current_window(2, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2023, 1, 1, 0, 0, 0))
        self.assertEqual(stop, datetime(2023, 3, 1, 0, 0, 0)) 

    def test_months_over_year_boundary(self):
        now = datetime(2023, 12, 15, 12, 15, 15)
        start, stop = get_current_window(1, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2023, 12, 1, 0, 0, 0))
        self.assertEqual(stop, datetime(2024, 1, 1, 0, 0, 0))    

    def test_get_current_window_days_cross_year(self):
        now = datetime(2023, 12, 31, 12, 15, 15)
        start, stop = get_current_window(2, TimeUnit.DAYS, now)
        self.assertEqual(start, datetime(2023, 12, 31, 0, 0, 0))
        self.assertEqual(stop, datetime(2024, 1, 2, 0, 0, 0)) 

    def test_get_current_window_hours_cross_day(self):
        now = datetime(2023, 10, 3, 23, 15, 15)
        start, stop = get_current_window(3, TimeUnit.HOURS, now)
        self.assertEqual(start, datetime(2023, 10, 3, 20, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 3, 23, 0, 0))

    def test_bad_intervals(self):
        self.assertRaises(ValueError, get_current_window, -1, TimeUnit.HOURS)
        self.assertRaises(TypeError, get_current_window, 0.0, TimeUnit.HOURS)

if __name__ == '__main__':
    unittest.main()


