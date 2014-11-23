from tests import ClientTest, expect
from tests.factory.news_category import NewsCategoryFactory
from models.news_category import News_Category


class AdminNewsCategoryModuleTestTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        News_Category.objects.delete()
        pass

    def test_get_list_news_category_should_response_status_200(self):
        resp = self.get('/admin/news_category/')
        expect(resp.status_int).to_equal(200)

    def test_get_exist_news_category_response_status_200(self):
        news_category = NewsCategoryFactory.create()
        resp = self.get('/admin/news_category/' + str(news_category.id))
        expect(resp.status_int).to_equal(200)

    def test_get_exist_news_category_response_correct_data(self):
        news_category = NewsCategoryFactory.create()
        resp = self.get('/admin/news_category/' + str(news_category.id))
        expect(resp).to_include(news_category.name)

    def test_get_not_exist_news_category_response_status_404(self):
        resp = self.get('/admin/news_category/1001')
        expect(resp.status_int).to_equal(404)

    def test_create_a_news_category_should_response_status_201(self):
        data = NewsCategoryFactory.attributes()
        resp = self.post('/admin/news_category/', data)
        expect(resp.status_int).to_equal(201)

    def test_create_a_news_category_should_response_correct_data(self):
        data = NewsCategoryFactory.attributes()
        resp = self.post('/admin/news_category/', data)
        expect(resp).to_include(data.get('name'))

    def test_update_an_existing_news_category_should_response_status_200(self):
        news_category = NewsCategoryFactory.create()
        data = NewsCategoryFactory.attributes()
        resp = self.post('/admin/news_category/' + str(news_category.id) + '/update', data)
        expect(resp.status_int).to_equal(200)

    def test_update_an_existing_news_category_should_be_done(self):
        news_category = NewsCategoryFactory.create()
        data = NewsCategoryFactory.attributes()
        resp = self.post('/admin/news_category/' + str(news_category.id) + '/update', data)
        news_category.reload()
        expect(news_category.name).to_equal(data.get('name'))
        expect(news_category.image).to_include(data.get('image'))

    def test_update_not_existing_news_category_should_response_status_404(self):
        data = NewsCategoryFactory.attributes()
        resp = self.post('/admin/news_category/1001/update', data)
        expect(resp.status_int).to_equal(404)

    def test_delete_existing_news_category_should_response_status_200(self):
        news_category = NewsCategoryFactory.create()
        resp = self.post('/admin/news_category/' + str(news_category.id) + '/delete',{})
        expect(resp.status_int).to_equal(200)

    def test_delete_exist_news_category_should_be_done(self):
        news_category = NewsCategoryFactory.create()
        resp = self.post('/admin/news_category/' + str(news_category.id) + '/delete',{})
        expect(len(News_Category.objects(id=news_category.id))).to_equal(0)

