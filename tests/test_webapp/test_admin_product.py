from tests import ClientTest, expect
from tests.factory.product import ProductFactory
from tests.factory.category import CategoryFactory
from tests.factory.brand import BrandFactory
from models.product import Product
from models.category import Category

class AdminProductModuleTestTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        Product.objects.delete()
        pass

    def test_get_list_product_should_response_status_200(self):
        resp = self.get('/admin/product/')
        expect(resp.status_int).to_equal(200)      

    def test_get_exist_product_should_response_status_200(self):
        product = ProductFactory.create()
        resp = self.get('/admin/product/'+str(product.id))
        expect(resp.status_int).to_equal(200)
    
    def test_get_exist_product_should_response_correct_data(self):
        product = ProductFactory.create()
        resp = self.get('/admin/product/'+str(product.id))
        expect(resp).to_include(product.name)
        expect(resp).to_include(product.sku)
        expect(resp).to_include(unicode(product.category.name))
        expect(resp).to_include(unicode(product.brand.name))
        expect(resp).to_include(unicode(product.price))
        expect(resp).to_include(str(product.selling_price))
        expect(resp).to_include(str(product.discount))
    
    def test_get_not_exist_product_should_response_status_404(self):
        resp = self.get('/admin/product/1000')
        expect(resp.status_int).to_equal(404)

    def test_create_product_should_response_status_201(self):
        product = ProductFactory.attributes()
        category = CategoryFactory.create()
        brand = BrandFactory.create()
        product['category'] = category.id
        product['brand'] = brand.id
        resp = self.post('/admin/product/',product)
        expect(resp.status_int).to_equal(201)

    def test_create_product_should_response_correct_data(self):
        product = ProductFactory.attributes()
        category = CategoryFactory.create()
        brand = BrandFactory.create()
        product['category'] = category.id
        product['brand'] = brand.id
        resp = self.post('/admin/product/',product)
        expect(resp).to_include(product['name'])
        expect(resp).to_include(product['sku'])
        expect(resp).to_include(unicode(category.name))
        expect(resp).to_include(unicode(brand.name))
        expect(resp).to_include(unicode(product['price']))
        expect(resp).to_include(str(product['selling_price']))
        expect(resp).to_include(str(product['discount']))

    def test_create_product_with_no_name_should_response_status_400(self):
        product = ProductFactory.attributes()
        del product['name']
        resp = self.post('/admin/product/',product)
        expect(resp.status_int).to_equal(400)

    def test_update_exist_product_should_response_status_200(self):
        product = ProductFactory.create()
        data = ProductFactory.attributes()
        del data['category']
        del data['brand']
        resp = self.post('/admin/product/' + str(product.id) + '/update', data)
        expect(resp.status_int).to_equal(200)

    def test_update_an_exist_product_should_be_done(self):
        product = ProductFactory.create()
        data = ProductFactory.attributes()
        del data['category']
        del data['brand']
        resp = self.post('/admin/product/' + str(product.id) + '/update', data)
        product.reload()
        expect(product.name).to_equal(data.get('name'))
        expect(product.sku).to_include(data.get('sku'))
        expect(resp).to_include(unicode(data.get('price')))
        expect(resp).to_include(data.get('selling_price'))
        expect(resp).to_include(data.get('discount'))

    def test_update_not_exist_product_should_response_status_404(self):
        data = ProductFactory.attributes()
        resp = self.post('/admin/product/1001/update', data)
        expect(resp.status_int).to_equal(404)

    def test_delete_exist_product_should_response_status_200(self):
        product = ProductFactory.create()
        resp = self.post('/admin/product/' + str(product.id) + '/delete',{})
        expect(resp.status_int).to_equal(200)

    def test_delete_exist_product_should_be_done(self):
        product = ProductFactory.create()
        resp = self.post('/admin/product/' + str(product.id) + '/delete',{})
        expect(len(Product.objects(id=product.id))).to_equal(0)

    def test_delete_not_exist_product_should_response_status_404(self):
        resp = self.post('/admin/product/1001/delete', {})
        expect(resp.status_int).to_equal(404)


