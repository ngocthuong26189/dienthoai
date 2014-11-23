from tests import ClientTest, expect, TestApp
from tests.factory.user import UserFactory
from models.user import User


class CurrentUserTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        User.objects.delete()
        pass

    def test_get_current_user(self):
        user = UserFactory.create()
        resp = self.get('/api/v1/user/self', headers={'REMOTE_USER': str(user.id)})
        expect(resp).to_include(user.username)
        expect(resp.status_int).to_equal(200)

