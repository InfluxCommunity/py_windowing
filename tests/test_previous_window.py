import unittest
from datetime import datetime
import sys
sys.path.append('../src/')
from src.windowing import get_next_window, get_current_window, get_previous_window, TimeUnit

class TestPreviousWindow(unittest.TestCase):

    def test_get_previous_window_minutes(self):
        now = datetime(2023, 10, 3, 12, 15)

        # Test minutes
        start, stop = get_previous_window(1, TimeUnit.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12, 14))
        self.assertEqual(stop, datetime(2023, 10, 3, 12, 15))

    def test_get_previous_cross_day(self):
        now = datetime(2023, 10, 3, 0, 1)

        # Test minutes
        start, stop = get_previous_window(10, TimeUnit.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 2, 23, 50))
        self.assertEqual(stop, datetime(2023, 10, 3, 0, 0))
    
    def test_get_previous_months(self):
        now = datetime(2023, 10, 3, 0, 1)
        start, stop = get_previous_window(1, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2023, 9, 1, 0, 0))
        self.assertEqual(stop, datetime(2023, 10, 1, 0, 0))
        
        # cross a year
        now = datetime(2023, 1, 3, 0, 1)
        start, stop = get_previous_window(1, TimeUnit.MONTHS, now)
        self.assertEqual(start, datetime(2022, 12, 1, 0, 0))
        self.assertEqual(stop, datetime(2023, 1, 1, 0, 0))

if __name__ == '__main__':
    unittest.main()


