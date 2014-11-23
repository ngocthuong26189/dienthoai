from tests import ClientTest, expect
from tests.factory.brand import BrandFactory
from models.brand import Brand


class AdminBrandModuleTestTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        Brand.objects.delete()
        pass

    def test_get_list_brand_should_response_status_200(self):
        resp = self.get('/admin/brand/')
        expect(resp.status_int).to_equal(200)

    def test_get_exist_brand_response_status_200(self):
        brand = BrandFactory.create()
        resp = self.get('/admin/brand/' + str(brand.uid))
        expect(resp.status_int).to_equal(200)

    def test_get_exist_brand_response_correct_data(self):
        brand = BrandFactory.create()
        resp = self.get('/admin/brand/' + str(brand.uid))
        expect(resp).to_include(brand.name)

    def test_get_not_exist_brand_response_status_404(self):
        resp = self.get('/admin/brand/1001')
        expect(resp.status_int).to_equal(404)

    def test_create_a_brand_should_response_status_201(self):
        data = BrandFactory.attributes()
        resp = self.post('/admin/brand/', data)
        expect(resp.status_int).to_equal(201)

    def test_create_a_brand_should_response_correct_data(self):
        data = BrandFactory.attributes()
        resp = self.post('/admin/brand/', data)
        expect(resp).to_include(data.get('name'))

    def test_update_an_existing_brand_should_response_status_200(self):
        brand = BrandFactory.create()
        data = BrandFactory.attributes()
        resp = self.post('/admin/brand/' + str(brand.uid) + '/update', data)
        expect(resp.status_int).to_equal(200)

    def test_update_an_existing_brand_should_be_done(self):
        brand = BrandFactory.create()
        data = BrandFactory.attributes()
        resp = self.post('/admin/brand/' + str(brand.uid) + '/update', data)
        brand.reload()
        expect(brand.name).to_equal(data.get('name'))
        expect(brand.image).to_include(data.get('image'))

    def test_update_not_existing_brand_should_response_status_404(self):
        data = BrandFactory.attributes()
        resp = self.post('/admin/brand/1001/update', data)
        expect(resp.status_int).to_equal(404)

    def test_delete_existing_user_should_response_status_200(self):
        brand = BrandFactory.create()
        resp = self.post('/admin/brand/' + str(brand.uid) + '/delete',{})
        expect(resp.status_int).to_equal(200)

    def test_delete_exist_user_should_be_done(self):
        brand = BrandFactory.create()
        resp = self.post('/admin/brand/' + str(brand.uid) + '/delete',{})
        expect(len(Brand.objects(uid=brand.uid))).to_equal(0)

