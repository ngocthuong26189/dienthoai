from tests import ClientTest, expect
from tests.factory.slider import SliderFactory
from tests.factory.banner import BannerFactory
from models.slider import Slider


class AdminSliderModuleTestTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        Slider.objects.delete()
        pass

    def test_get_list_slider_should_response_status_200(self):
        resp = self.get('/admin/slider/')
        expect(resp.status_int).to_equal(200)

    def test_get_exist_slider_response_status_200(self):
        slider = SliderFactory.create()
        resp = self.get('/admin/slider/' + str(slider.id))
        expect(resp.status_int).to_equal(200)

    def test_get_exist_slider_response_correct_data(self):
        slider = SliderFactory.create()
        resp = self.get('/admin/slider/' + str(slider.id))
        expect(resp).to_include(slider.name)

    def test_get_not_exist_slider_response_status_404(self):
        resp = self.get('/admin/slider/1001')
        expect(resp.status_int).to_equal(404)

    def test_create_a_slider_should_response_status_201(self):
        data = SliderFactory.attributes()
        resp = self.post('/admin/slider/', data)
        expect(resp.status_int).to_equal(201)

    def test_create_a_slider_should_response_correct_data(self):
        data = SliderFactory.attributes()
        resp = self.post('/admin/slider/', data)
        expect(resp).to_include(data.get('name'))

    def test_update_an_existing_slider_should_response_status_200(self):
        slider = SliderFactory.create()
        data = SliderFactory.attributes()
        resp = self.post('/admin/slider/' + str(slider.id) + '/update', data)
        expect(resp.status_int).to_equal(200)

    def test_update_an_existing_slider_should_be_done(self):
        slider = SliderFactory.create()
        data = SliderFactory.attributes()
        resp = self.post('/admin/slider/' + str(slider.id) + '/update', data)
        slider.reload()
        expect(slider.name).to_equal(data.get('name'))
        expect(slider.description).to_equal(data.get('description'))

    def test_update_not_existing_slider_should_response_status_404(self):
        data = SliderFactory.attributes()
        resp = self.post('/admin/slider/1001/update', data)
        expect(resp.status_int).to_equal(404)

    def test_delete_existing_slider_should_response_status_200(self):
        slider = SliderFactory.create()
        resp = self.post('/admin/slider/' + str(slider.id) + '/delete',{})
        expect(resp.status_int).to_equal(200)

    def test_delete_exist_slider_should_be_done(self):
        slider = SliderFactory.create()
        resp = self.post('/admin/slider/' + str(slider.id) + '/delete',{})
        expect(len(Slider.objects(id=slider.id))).to_equal(0)

