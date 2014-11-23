from tests import ClientTest, expect
from tests.factory.category import CategoryWithParentFactory,CategoryFactory
from models.category import Category


class AdminCategoryModuleTestTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        Category.objects.delete()
        pass

    def test_get_list_category_should_response_status_200(self):
        resp = self.get('/admin/category/')
        expect(resp.status_int).to_equal(200)

    def test_get_exist_category_response_status_200(self):
        category = CategoryWithParentFactory.create()
        resp = self.get('/admin/category/' + str(category.id))
        expect(resp.status_int).to_equal(200)

    def test_get_exist_category_response_correct_data(self):
        category = CategoryWithParentFactory.create()
        resp = self.get('/admin/category/' + str(category.id))
        expect(resp).to_include(category.name)
        expect(resp).to_include(category.image)

    def test_get_not_exist_category_response_status_404(self):
        resp = self.get('/admin/category/1001')
        expect(resp.status_int).to_equal(404)

    def test_create_a_category_with_empty_parent_should_response_status_201(self):
        category = CategoryFactory.attributes()
        resp = self.post('/admin/category/', category)
        expect(resp.status_int).to_equal(201)

    def test_create_a_category_with_parent_should_response_status_201(self):
        parent = CategoryFactory.create()
        category = CategoryWithParentFactory.attributes()
        category['parent']=parent.id
        resp = self.post('/admin/category/', category)
        expect(resp.status_int).to_equal(201)

    def test_create_a_category_with_not_enough_data_properties_sould_response_status_400(self):
        category = CategoryFactory.attributes()
        del category['name']
        resp = self.post('/admin/category/', category)
        expect(resp.status_int).to_equal(400)
    
    def test_create_a_category_with_exist_category_name_sould_response_status_400(self):
        category = CategoryWithParentFactory.create()
        data = CategoryFactory.attributes()
        data['name'] = category.name
        resp = self.post('/admin/category/', data)
        expect(resp.status_int).to_equal(400)
    
    def test_create_a_category_with_empty_parent_should_response_correct_data(self):
        category = CategoryFactory.attributes()
        resp = self.post('/admin/category/', category)
        expect(resp).to_include(category.get('name'))
        expect(resp).to_include(category.get('image'))

    def test_create_a_category_with_parent_should_response_correct_data(self):
        parent = CategoryFactory.create()
        category = CategoryWithParentFactory.attributes()
        category['parent'] =  parent.id
        resp = self.post('/admin/category/', category)
        expect(resp).to_include(category.get('name'))
        expect(resp).to_include(category.get('image'))
        expect(resp).to_include(unicode(category.get('parent')))

    def test_update_an_exist_category_should_response_status_200(self):
        category = CategoryWithParentFactory.create()
        data = CategoryWithParentFactory.attributes()
        parent = CategoryFactory.create()
        data['parent'] = str(parent['id'])
        resp = self.post('/admin/category/' + str(category.id) + '/update', data)
        expect(resp.status_int).to_equal(200)
    
    def test_update_an_category_not_exist_should_return_status_400(self):    
        data = CategoryWithParentFactory.attributes()
        resp = self.post('/admin/category/' + '1' + '/update', data)
        expect(resp.status_int).to_equal(400)

    def test_update_an_category_not_exist_parent_should_return_status_400(self):
        category = CategoryWithParentFactory.create()
        data = CategoryWithParentFactory.attributes()
        data['parent'] = str(category['parent']['id']) + "10"
        resp = self.post('/admin/category/' + str(category.id) + '/update', data)
        expect(resp.status_int).to_equal(400)

    def test_update_an_category_vicious_cycle_should_return_status_400(self):
        category = CategoryWithParentFactory.create()
        parent = category.parent
        data = CategoryWithParentFactory.attributes()
        data['parent'] = category.id;
        resp = self.post('/admin/category/' + str(parent.id) + '/update', data)
        expect(resp.status_int).to_equal(400)

    def test_update_an_category_with_parent_is_sefl_should_return_status_400(self):
        category = CategoryWithParentFactory.create()
        data = CategoryWithParentFactory.attributes()
        data['parent'] = category.id;
        resp = self.post('/admin/category/' + str(category.id) + '/update', data)
        expect(resp.status_int).to_equal(400)
        
    def test_update_an_exist_category_should_be_done(self):
        category = CategoryWithParentFactory.create()
        data = CategoryWithParentFactory.attributes()
        data['parent'] = str(category['parent']['id'])
        resp = self.post('/admin/category/' + str(category.id) + '/update', data)
        expect(resp).to_include(data.get('parent'))
        expect(resp).to_include(data.get('name'))
        expect(resp).to_include(data.get('image'))
        
    def test_delete_exist_category_should_be_done(self):
        category = CategoryFactory.create()
        resp = self.post('/admin/category/' + str(category.id) + '/delete',{})
        expect(len(Category.objects(id=category.id))).to_equal(0)

    def test_delete_not_exist_category_should_response_status_404(self):
        resp = self.post('/admin/category/111/delete', {})
        expect(resp.status_int).to_equal(404)    


