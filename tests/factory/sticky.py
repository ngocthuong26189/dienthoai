import factory
from factory.mongoengine import MongoEngineFactory
from models import sticky

class StickyFactory(MongoEngineFactory):

    class Meta:
        model = sticky.Sticky

    name = factory.Sequence(lambda n: 'sticky-{0}'.format(n))
    image = factory.Sequence(lambda n: 'sticky-{0}.png'.format(n))
