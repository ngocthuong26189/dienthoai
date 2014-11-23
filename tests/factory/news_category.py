import factory
from factory.mongoengine import MongoEngineFactory
from models import news_category

class NewsCategoryFactory(MongoEngineFactory):

    class Meta:
        model = news_category.News_Category

    name = factory.Sequence(lambda n: 'sticky-{0}'.format(n))
    image = factory.Sequence(lambda n: 'sticky-{0}.png'.format(n))
