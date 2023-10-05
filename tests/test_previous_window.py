import unittest
from datetime import datetime
import sys
sys.path.append('../src/')
from src.windowing import get_next_window, get_current_window, get_previous_window, IntervalType

class TestNextWindow(unittest.TestCase):

    def test_get_previous_window_minutes(self):
        now = datetime(2023, 10, 3, 12, 15)

        # Test minutes
        start, stop = get_previous_window(1, IntervalType.MINUTES, now)
        self.assertEqual(start, datetime(2023, 10, 3, 12, 14))
        self.assertEqual(stop, datetime(2023, 10, 3, 12, 15))
        
if __name__ == '__main__':
    unittest.main()


