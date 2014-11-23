from tests import ClientTest, expect
from tests.factory.sticky import StickyFactory
from models.sticky import Sticky


class AdminStickyModuleTestTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        Sticky.objects.delete()
        pass

    def test_get_list_sticky_should_response_status_200(self):
        resp = self.get('/admin/sticky/')
        expect(resp.status_int).to_equal(200)

    def test_get_exist_sticky_response_status_200(self):
        sticky = StickyFactory.create()
        resp = self.get('/admin/sticky/' + str(sticky.id))
        expect(resp.status_int).to_equal(200)

    def test_get_exist_sticky_response_correct_data(self):
        sticky = StickyFactory.create()
        resp = self.get('/admin/sticky/' + str(sticky.id))
        expect(resp).to_include(sticky.name)

    def test_get_not_exist_sticky_response_status_404(self):
        resp = self.get('/admin/sticky/1001')
        expect(resp.status_int).to_equal(404)

    def test_create_a_sticky_should_response_status_201(self):
        data = StickyFactory.attributes()
        resp = self.post('/admin/sticky/', data)
        expect(resp.status_int).to_equal(201)

    def test_create_a_sticky_should_response_correct_data(self):
        data = StickyFactory.attributes()
        resp = self.post('/admin/sticky/', data)
        expect(resp).to_include(data.get('name'))

    def test_update_an_existing_sticky_should_response_status_200(self):
        sticky = StickyFactory.create()
        data = StickyFactory.attributes()
        resp = self.post('/admin/sticky/' + str(sticky.id) + '/update', data)
        expect(resp.status_int).to_equal(200)

    def test_update_an_existing_sticky_should_be_done(self):
        sticky = StickyFactory.create()
        data = StickyFactory.attributes()
        resp = self.post('/admin/sticky/' + str(sticky.id) + '/update', data)
        sticky.reload()
        expect(sticky.name).to_equal(data.get('name'))
        expect(sticky.image).to_include(data.get('image'))

    def test_update_not_existing_sticky_should_response_status_404(self):
        data = StickyFactory.attributes()
        resp = self.post('/admin/sticky/1001/update', data)
        expect(resp.status_int).to_equal(404)

    def test_delete_existing_sticky_should_response_status_200(self):
        sticky = StickyFactory.create()
        resp = self.post('/admin/sticky/' + str(sticky.id) + '/delete',{})
        expect(resp.status_int).to_equal(200)

    def test_delete_exist_sticky_should_be_done(self):
        sticky = StickyFactory.create()
        resp = self.post('/admin/sticky/' + str(sticky.id) + '/delete',{})
        expect(len(Sticky.objects(id=sticky.id))).to_equal(0)

