from tests import ClientTest, expect
class BaseRouteUrlTest(ClientTest):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_home_page_should_return_status_200(self):
        resp = self.get('/')
        expect(resp.status).to_equal("200 OK")

    def test_go_to_incorrect_url_should_return_status_404(self):
        resp = self.get('/whatever')
        expect(resp.status).to_equal("404 NOT FOUND")
