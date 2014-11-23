import unittest
import md5
import mongoengine

from models import user
from tests.factory.user import UserFactory
from tests import expect


class UserModelTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # delete test data
        user.User.objects.delete()

    def test_create_user_should_work(self):
        attr = UserFactory.attributes()
        u = user.create(attr)
        expect(u.username).to_equal(attr.get('username'))
        expect(u.email).to_equal(attr.get('email'))
        expect(u.password).to_equal(md5.new(attr.get('password')).hexdigest())

    def test_duplication_error(self):
        u = UserFactory.create()
        with expect.error_to_happen(mongoengine.NotUniqueError): user.create({"username": u.username})

    def test_get_data_from_exists_user(self):
        data = UserFactory.create()
        u = user.get(data.username)
        expect(u.username).to_equal(data.username)
        expect(u.email).to_equal(data.email)

    def test_get_user_not_found(self):
        u = user.get("not_a_exist_user")
        expect(u).to_be_null()
