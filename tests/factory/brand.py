import factory
from factory.mongoengine import MongoEngineFactory
from models import brand

class BrandFactory(MongoEngineFactory):

    class Meta:
        model = brand.Brand

    name = factory.Sequence(lambda n: 'brand-{0}'.format(n))
    image = factory.Sequence(lambda n: 'brand-{0}.png'.format(n))
