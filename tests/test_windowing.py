import unittest
from datetime import datetime
import sys
sys.path.append('../src/')
from src.windowing import get_next_window, get_current_window, TimeUnit

class TestWindowing(unittest.TestCase):
    def test_bad_intervals(self):
        self.assertRaises(ValueError, get_current_window, -1, TimeUnit.HOURS)
        self.assertRaises(TypeError, get_current_window, 0.0, TimeUnit.HOURS)
        
if __name__ == '__main__':
    unittest.main()


