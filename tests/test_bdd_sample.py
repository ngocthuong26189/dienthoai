import unittest
import os
from tests import expect

class BddSampleTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_expected_result_is_pass(self):
        expect(1).to_equal(1)

    def test_expected_result_is_incorrect(self):
        expect(2).not_to_equal(1)
