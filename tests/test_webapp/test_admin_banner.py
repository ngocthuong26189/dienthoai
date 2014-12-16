from tests import ClientTest, expect
from tests.factory.banner import BannerFactory
from tests.factory.slider import SliderFactory
from models.banner import Banner


class AdminBannerModuleTestTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        Banner.objects.delete()
        pass

    def test_get_list_banner_should_response_status_200(self):
        resp = self.get('/admin/banner/')
        expect(resp.status_int).to_equal(200)

    def test_get_exist_banner_response_status_200(self):
        banner = BannerFactory.create()
        resp = self.get('/admin/banner/' + str(banner.id))
        expect(resp.status_int).to_equal(200)

    def test_get_exist_banner_response_correct_data(self):
        banner = BannerFactory.create()
        resp = self.get('/admin/banner/' + str(banner.id))
        expect(resp).to_include(banner.name)

    def test_get_not_exist_banner_response_status_404(self):
        resp = self.get('/admin/banner/1001')
        expect(resp.status_int).to_equal(404)

    def test_create_a_banner_should_response_status_201(self):
        data = BannerFactory.attributes()
        resp = self.post('/admin/banner/', data)
        expect(resp.status_int).to_equal(201)

    def test_create_a_banner_should_response_correct_data(self):
        data = BannerFactory.attributes()
        resp = self.post('/admin/banner/', data)
        expect(resp).to_include(data.get('name'))

    def test_update_an_existing_banner_should_response_status_200(self):
        banner = BannerFactory.create()
        data = BannerFactory.attributes()
        resp = self.post('/admin/banner/' + str(banner.id) + '/update', data)
        expect(resp.status_int).to_equal(200)

    def test_update_an_existing_banner_should_be_done(self):
        banner = BannerFactory.create()
        data = BannerFactory.attributes()
        resp = self.post('/admin/banner/' + str(banner.id) + '/update', data)
        banner.reload()
        expect(banner.name).to_equal(data.get('name'))
        expect(banner.image).to_include(data.get('image'))

    def test_update_not_existing_banner_should_response_status_404(self):
        data = BannerFactory.attributes()
        resp = self.post('/admin/banner/1001/update', data)
        expect(resp.status_int).to_equal(404)

    def test_delete_existing_banner_should_response_status_200(self):
        banner = BannerFactory.create()
        resp = self.post('/admin/banner/' + str(banner.id) + '/delete',{})
        expect(resp.status_int).to_equal(200)

    def test_delete_exist_banner_should_be_done(self):
        banner = BannerFactory.create()
        resp = self.post('/admin/banner/' + str(banner.id) + '/delete',{})
        expect(len(Banner.objects(id=banner.id))).to_equal(0)

