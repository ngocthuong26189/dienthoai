import factory
from factory.mongoengine import MongoEngineFactory
from models import category

class CategoryFactory(MongoEngineFactory):

    class Meta:
        model = category.Category

    name = factory.Sequence(lambda category: 'category_name{0}'.format(category))
    image = factory.LazyAttribute(lambda category: '/img/{0}'.format(category.name))

class CategoryWithParentFactory(CategoryFactory):
    parent = factory.SubFactory(CategoryFactory)
