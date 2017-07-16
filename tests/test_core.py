"""
Test cases for SemVerCore
"""

import unittest
import libsemver

class TestSemVerCore(unittest.TestCase):
    """Test cases for SemVerCore"""

    def test_creation(self):
        """
        Test creating a SemVerCore object with defaults
        and verifying that the fields read back as expected
        """
        obj = libsemver.SemVerCore(1, 0, 2)

        self.assertTrue(obj.major == 1)
        self.assertTrue(obj.minor == 0)
        self.assertTrue(obj.patch == 2)
        self.assertTrue(obj.prerelease is None)
        self.assertTrue(obj.build_metadata is None)


    def test_setting(self):
        """
        Test creating a SemVerCore object and setting the
        individual fields
        """
        obj = libsemver.SemVerCore(0, 0, 0)

        obj.major = 1
        self.assertTrue(obj.major == 1)

        obj.minor = 2
        self.assertTrue(obj.minor == 2)

        obj.patch = 3
        self.assertTrue(obj.patch == 3)


    def test_prerelease(self):
        """
        Test creating a SemVerCore object and setting the
        prerelease fields
        """
        obj = libsemver.SemVerCore(0, 0, 0)

        # Verify setting to None returns None
        obj.prerelease = None
        self.assertTrue(obj.prerelease is None)

        # Verify setting to an empty list returns None
        obj.prerelease = []
        self.assertTrue(obj.prerelease is None)

        # Verify conversion from string to integer
        obj.prerelease = ['ab', '12', '0xcd']
        self.assertTrue(obj.prerelease == ['ab', 12, '0xcd'])

        # Verify that an all integer value gets treated as integers
        obj.prerelease = ['12', '34', '56']
        self.assertTrue(obj.prerelease == [12, 34, 56])

        # Verify that periods in the elements cause errors
        with self.assertRaises(AssertionError):
            obj.prerelease = ['a.b.c.d']


    def test_build_metadata(self):
        """
        Test creating a SemVerCore object and setting the
        prerelease fields
        """
        obj = libsemver.SemVerCore(0, 0, 0)

        # Verify setting to None returns None
        obj.build_metadata = None
        self.assertTrue(obj.build_metadata is None)

        # Verify setting to an empty list returns None
        obj.build_metadata = []
        self.assertTrue(obj.build_metadata is None)

        # Verify strings are retained as such
        obj.build_metadata = ['ab', '12', '0xcd']
        self.assertTrue(obj.build_metadata == ['ab', '12', '0xcd'])

        # Verify that an all integer value gets converted to strings
        obj.build_metadata = ['12', '34', '56']
        self.assertTrue(obj.build_metadata == ['12', '34', '56'])

        # Verify that periods in the elements cause errors
        with self.assertRaises(AssertionError):
            obj.build_metadata = ['a.b.c.d']


    def test_string_output(self):
        """
        Test the string formatting
        """
        obj = libsemver.SemVerCore(1, 2, 3)

        # Verify default output string
        self.assertTrue(str(obj) == '1.2.3')

        # Verify prerelease string
        obj.prerelease = ['ab', '12', '0xcd']
        self.assertTrue(str(obj) == '1.2.3-ab.12.0xcd')

        # Verify build metadata
        obj.build_metadata = ['2017', '07', '10']
        self.assertTrue(str(obj) == '1.2.3-ab.12.0xcd+2017.07.10')


