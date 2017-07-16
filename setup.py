#!/usr/bin/env python

from setuptools import setup
import unittest

def semver_tests():
    """Return a test suite generated from the files in tests/test_*.py"""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(name='libsemver',
      version='0.1.0',
      description='Python Semantic Version Library',
      url='http://github.com/nirenjan/libsemver',
      author='Nirenjan Krishnan',
      author_email='nirenjan@gmail.com',
      license='MIT',
      packages=['libsemver'],
      test_suite='setup.semver_tests',
      zip_safe=False)
