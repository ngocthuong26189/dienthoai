from tests import ClientTest, expect
from tests.factory.user import UserFactory
from models.user import User


class AdminUserModuleTestTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        User.objects.delete()
        pass

    def test_get_list_user_should_response_status_200(self):
        resp = self.get('/admin/user/')
        expect(resp.status_int).to_equal(200)

    def test_get_exist_user_response_status_200(self):
        user = UserFactory.create()
        resp = self.get('/admin/user/' + str(user.uid))
        expect(resp.status_int).to_equal(200)

    def test_get_exist_user_response_correct_data(self):
        user = UserFactory.create()
        resp = self.get('/admin/user/' + str(user.uid))
        expect(resp).to_include(user.username)
        expect(resp).to_include(user.email)

    def test_get_not_exist_user_response_status_404(self):
        resp = self.get('/admin/user/1001')
        expect(resp.status_int).to_equal(404)

    def test_create_an_user_should_response_status_201(self):
        data = UserFactory.attributes()
        resp = self.post('/admin/user/', data)
        expect(resp.status_int).to_equal(201)

    def test_create_an_user_should_response_correct_data(self):
        data = UserFactory.attributes()
        resp = self.post('/admin/user/', data)
        expect(resp).to_include(data.get('username'))
        expect(resp).to_include(data.get('email'))


    def test_create_an_exist_username_should_response_duplication_error(self):
        data = UserFactory.attributes()
        user = UserFactory.create(**data)
        resp = self.post('/admin/user/', data)
        expect(resp.status_int).to_equal(400)
        expect(resp).to_include('Duplicated')

    def test_update_an_exist_user_should_response_status_200(self):
        user = UserFactory.create()
        data = UserFactory.attributes()
        resp = self.post('/admin/user/' + str(user.uid) + '/update', data)
        expect(resp.status_int).to_equal(200)

    def test_update_an_exist_user_should_be_done(self):
        user = UserFactory.create()
        data = UserFactory.attributes()
        resp = self.post('/admin/user/' + str(user.uid) + '/update', data)
        user.reload()
        expect(user.username).to_equal(data.get('username'))
        expect(user.email).to_include(data.get('email'))

    def test_update_not_exist_user_should_response_status_404(self):
        data = UserFactory.attributes()
        resp = self.post('/admin/user/1001/update', data)
        expect(resp.status_int).to_equal(404)

    def test_delete_exist_user_should_response_status_200(self):
        user = UserFactory.create()
        resp = self.post('/admin/user/' + str(user.uid) + '/delete',{})
        expect(resp.status_int).to_equal(200)

    def test_delete_exist_user_should_be_done(self):
        user = UserFactory.create()
        resp = self.post('/admin/user/' + str(user.uid) + '/delete',{})
        expect(len(User.objects(uid=user.uid))).to_equal(0)


    def test_delete_not_exist_user_should_response_status_404(self):
        resp = self.post('/admin/user/1001/delete', {})
        expect(resp.status_int).to_equal(404)

    def test_access_to_create_form_should_response_status_200(self):
        resp = self.get('/admin/user/create')
        expect(resp.status_int).to_equal(200)

    def test_access_to_edit_form_of_exist_user_should_response_status_200(self):
        user = UserFactory.create()
        resp = self.get('/admin/user/' + str(user.uid) + '/edit')
        expect(resp.status_int).to_equal(200)

    def test_access_to_edit_form_of_not_exist_user_should_response_status_404(self):
        resp = self.get('/admin/user/1001/edit')
        expect(resp.status_int).to_equal(404)
