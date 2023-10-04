import unittest
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run unittests.')
    parser.add_argument('--verbose', action='store_true', help='Run tests in verbose mode.')
    args = parser.parse_args()

    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    runner = unittest.TextTestRunner(verbosity=(2 if args.verbose else 1))
    runner.run(suite)
