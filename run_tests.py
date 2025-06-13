#!/usr/bin/env python3
"""
Test runner for the image recognition application.
"""

import unittest
import sys


def run_tests():
    """Run all tests and return the result."""
    test_suite = unittest.defaultTestLoader.discover('test')
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)