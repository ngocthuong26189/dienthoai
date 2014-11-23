import factory
from factory.mongoengine import MongoEngineFactory
from models import product
from tests.factory.category import CategoryFactory
from tests.factory.brand import BrandFactory


class ProductBasicFactory(MongoEngineFactory):

    class Meta:
        model = product.Product

    sku = factory.Sequence(lambda product: 'product_sku{0}'.format(product))
    name = factory.Sequence(lambda product: 'product_name{0}'.format(product))
    image = factory.LazyAttribute(lambda product: '/img/{0}'.format(product.name))
    price = factory.Sequence(lambda product: '{0}'.format(product))
    selling_price = factory.Sequence(lambda product: '{0}'.format(product))
    discount = factory.Sequence(lambda product: '{0}'.format(product))
   
class ProductFactory(ProductBasicFactory ,CategoryFactory, BrandFactory):
    
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
