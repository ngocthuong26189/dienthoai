import unittest
import mongoengine

from models import brand
from tests.factory.brand import BrandFactory
from tests import expect


class BrandModelTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # delete test data
        brand.Brand.objects.delete()

    def test_create_brand_should_work(self):
        attr = BrandFactory.attributes()
        b = brand.create(attr)
        expect(b.name).to_equal(attr.get('name'))

    def test_get_data_from_existing_brand(self):
        attr = BrandFactory.attributes()
        data = brand.create(attr)
        b = brand.get(data.uid)
        expect(b.name).to_equal(data.name)

    def test_get_brand_not_found(self):
        b = brand.get("whatever")
        expect(b).to_be_null()
