import unittest

from webtest import TestApp
from webapp import app


class BddSampleTest(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(app)

    def tearDown(self):
        pass

    def test_expected_result_is_pass(self):
        assert 1 is 1

    def test_expected_result_is_fail(self):
        assert 2 is not 1
