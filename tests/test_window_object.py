import unittest
from datetime import datetime
import sys
sys.path.append('../src/')
from src.windowing import Window, IntervalType

class TestWindowObject(unittest.TestCase):
    def test_create_window(self):
        now = datetime(2023, 10, 3, 12, 15, 15)
        w = Window(interval_length=1,interval_type=IntervalType.MINUTES,now=now)
        self.assertEqual(w.start, datetime(2023, 10, 3, 12, 15))
        self.assertEqual(w.stop, datetime(2023, 10, 3, 12, 16))

        w = Window(interval_length=10,interval_type=IntervalType.MINUTES,now=now)
        self.assertEqual(w.start, datetime(2023, 10, 3, 12, 10))
        self.assertEqual(w.stop, datetime(2023, 10, 3, 12, 20))

    def test_works_with_current_time(self):
        try:
            Window(interval_length=10,interval_type=IntervalType.MINUTES)
        except Exception as e:
            self.fail(f"Function crashed with {e}")

    def test_window_previous(self):
        now = datetime(2023, 10, 3, 12, 1, 15)
        w = Window(interval_length=1,interval_type=IntervalType.MINUTES,now=now).previous_window
        self.assertEqual(w.start, datetime(2023, 10, 3, 12, 0))
        self.assertEqual(w.stop, datetime(2023, 10, 3, 12, 1))

        w = w.previous_window
        self.assertEqual(w.start, datetime(2023, 10, 3, 11, 59))
        self.assertEqual(w.stop, datetime(2023, 10, 3, 12, 0))     

    def test_window_next(self):
        now = datetime(2023, 10, 3, 12, 57, 15)
        w = Window(interval_length=1,interval_type=IntervalType.MINUTES,now=now).next_window
        self.assertEqual(w.start, datetime(2023, 10, 3, 12, 58))
        self.assertEqual(w.stop, datetime(2023, 10, 3, 12, 59))

        w = w.next_window
        self.assertEqual(w.start, datetime(2023, 10, 3, 12, 59))
        self.assertEqual(w.stop, datetime(2023, 10, 3, 13, 0)) 

    def test_bad_arguments(self):
        with self.assertRaises(ValueError):
            Window(interval_length=-1, interval_type=IntervalType.HOURS)
        with self.assertRaises(ValueError):
            Window(interval_length=1, interval_type=None)
        with self.assertRaises(TypeError):
            Window(interval_length=0.0, interval_type=IntervalType.HOURS) 


if __name__ == '__main__':
    unittest.main()


