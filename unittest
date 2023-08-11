#!/usr/bin/env python3

# run_tests.py
import os
import sys
import unittest

# Add your project's root directory to the PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Discover and run the tests
loader = unittest.TestLoader()
test_suite = loader.discover('tests', pattern='test_*.py')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(test_suite)
