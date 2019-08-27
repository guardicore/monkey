import pytest
import unittest


class TestMonkeyBlackbox(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up all GCP machines...")

    @classmethod
    def tearDownClass(cls):
        print("Killing all GCP machines...")

    def test_1_plus_1(self):
        assert 1 + 1 == 2
