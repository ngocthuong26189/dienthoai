import unittest

from models.user import User, generate_encrypt_password
from tests.factory.user import UserFactory
from tests import expect
from services import identity

class AuthenticateTest(unittest.TestCase):
    def setUp(self):
        # Make user for test
        user1 = UserFactory.create(username="user1", password=generate_encrypt_password('testpass1'))
        user2 = UserFactory.create(username="user2", password=generate_encrypt_password('another'))

    def tearDown(self):
        User.objects.delete()

    def test_authentication_fail_with_wrong_password(self):
        result = identity.authenticate("user1", "wrongpass")
        expect(result).to_be_false()

    def test_authentication_fail_with_wrong_username(self):
        result = identity.authenticate("whoever", "wrongpass")
        expect(result).to_be_false()


    def test_authentication_success(self):
        result = identity.authenticate("user1", "testpass1")
        expect(result).to_be_true()
